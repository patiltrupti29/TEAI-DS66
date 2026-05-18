
# Stage 3

# Query Performance Analysis

## Existing Query

```sql
SELECT *
FROM notifications
WHERE studentID = 1042
AND isRead = false
ORDER BY createdAt DESC;
```

---

# Is This Query Correct?

Yes, the query is logically correct because it:

- Fetches notifications for a specific student
- Filters only unread notifications
- Sorts notifications by latest created date

However, it is inefficient for large datasets.

---

# Why Is This Query Slow?

The database currently contains:

- 50,000 students
- 5,000,000 notifications

Without proper indexing, the database performs:

- Full table scan
- Sorting operation on huge data
- High disk I/O
- Increased CPU usage

This increases query execution time significantly.

---

# Main Performance Problems

## 1. Full Table Scan

The database scans millions of rows to find matching records.

---

## 2. Sorting Cost

`ORDER BY createdAt DESC` requires sorting large datasets.

---

## 3. SELECT *

Fetching all columns increases:

- Memory usage
- Network transfer
- Query execution time

---

# Recommended Optimized Query

```sql
SELECT id,
       title,
       message,
       notificationType,
       createdAt
FROM notifications
WHERE studentID = 1042
AND isRead = false
ORDER BY createdAt DESC
LIMIT 50;
```

---

# Why This Query Is Better

## Improvements

- Fetches only required columns
- Uses LIMIT for pagination
- Reduces memory consumption
- Reduces network overhead
- Improves response time

---

# Recommended Index

## Composite Index

```sql
CREATE INDEX idx_notifications_student_read_created
ON notifications(studentID, isRead, createdAt DESC);
```

---

# Why Composite Index Helps

The query filters on:

1. studentID
2. isRead

and sorts on:

3. createdAt DESC

The composite index allows the database to:

- Quickly locate matching rows
- Avoid full table scans
- Avoid expensive sorting

---

# Likely Computational Cost

## Without Index

### Complexity

```text
O(N)
```

The database scans millions of rows.

---

## With Composite Index

### Complexity

```text
O(log N)
```

Search becomes significantly faster using indexed lookup.

---

# Should We Add Indexes on Every Column?

## Answer

No, adding indexes on every column is NOT effective.

---

# Why Adding Too Many Indexes Is Bad

## Problems

### 1. Increased Storage

Indexes consume additional disk space.

---

### 2. Slower INSERT/UPDATE/DELETE

Every index must also be updated during writes.

---

### 3. Higher Maintenance Cost

Too many indexes reduce overall database efficiency.

---

### 4. Unused Indexes Waste Resources

Indexes should only be created for:

- Frequently filtered columns
- Sorting columns
- Join conditions

---

# Best Practice

Create indexes only on:

- High-frequency query columns
- WHERE clause columns
- ORDER BY columns
- JOIN columns

---

# Query to Find Students Who Got Placement Notifications in Last 7 Days

## SQL Query

```sql
SELECT DISTINCT studentID
FROM notifications
WHERE notificationType = 'Placement'
AND createdAt >= NOW() - INTERVAL '7 days';
```

---

# Optimized Index for Placement Query

```sql
CREATE INDEX idx_notifications_type_created
ON notifications(notificationType, createdAt DESC);
```

---

# Additional Scalability Improvements

## 1. Pagination

Use:

```sql
LIMIT 50 OFFSET 0
```

to avoid loading large datasets.

---

## 2. Table Partitioning

Partition notifications table by:

- Month
- Year

This improves query speed.

---

## 3. Archiving Old Notifications

Move old notifications to archive tables.

---

## 4. Caching

Use Redis to cache frequently accessed notifications.

---

## 5. Read Replicas

Use read replicas for heavy read operations.

---

# Final Recommendation

For large-scale notification systems:

- Use composite indexes
- Avoid SELECT *
- Use pagination
- Avoid unnecessary indexes
- Archive old data
- Use caching and partitioning

These optimizations improve performance and scalability significantly.

---