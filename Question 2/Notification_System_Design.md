# Stage 2

# Persistent Storage Choice

## Recommended Database

### PostgreSQL (Relational Database)

PostgreSQL is recommended for the notification system because:

- Supports structured data with strong consistency
- Handles large-scale transactional systems efficiently
- Provides indexing for faster notification retrieval
- Supports JSON fields if flexible metadata is needed
- Reliable for read/write operations
- Supports pagination and filtering efficiently
- Easy integration with REST APIs

---

# Database Schema

## Table: users

```sql
CREATE TABLE users (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(150) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## Table: notifications

```sql
CREATE TABLE notifications (
    id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    type VARCHAR(50),
    priority VARCHAR(20) DEFAULT 'medium',
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_user
    FOREIGN KEY(user_id)
    REFERENCES users(id)
    ON DELETE CASCADE
);
```

---

# Indexing Strategy

## Create Indexes

```sql
CREATE INDEX idx_notifications_user_id
ON notifications(user_id);

CREATE INDEX idx_notifications_is_read
ON notifications(is_read);

CREATE INDEX idx_notifications_created_at
ON notifications(created_at DESC);
```

---

# Problems as Data Volume Increases

## 1. Slow Query Performance

### Problem

Fetching notifications becomes slow when millions of records exist.

### Solution

- Add indexes on:
  - user_id
  - is_read
  - created_at
- Use pagination with LIMIT and OFFSET

---

## 2. High Database Load

### Problem

Large number of read/write requests overloads the database.

### Solution

- Use caching with Redis
- Apply database connection pooling
- Separate read replicas

---

## 3. Storage Growth

### Problem

Notification data continuously increases.

### Solution

- Archive old notifications
- Delete expired notifications
- Use table partitioning

---

## 4. Real-Time Delivery Delays

### Problem

WebSocket delivery slows during heavy traffic.

### Solution

- Use message brokers:
  - RabbitMQ
  - Apache Kafka
- Use scalable WebSocket servers

---

# SQL Queries Based on REST APIs

# 1. Create Notification

## SQL Query

```sql
INSERT INTO notifications (
    id,
    user_id,
    title,
    message,
    type,
    priority
)
VALUES (
    'notif_101',
    'user_501',
    'Payment Successful',
    'Your payment of ₹1200 was successful.',
    'payment',
    'high'
);
```

---

# 2. Get All Notifications

## SQL Query

```sql
SELECT *
FROM notifications
WHERE user_id = 'user_501'
ORDER BY created_at DESC
LIMIT 10 OFFSET 0;
```

---

# 3. Get Notification By ID

## SQL Query

```sql
SELECT *
FROM notifications
WHERE id = 'notif_101';
```

---

# 4. Mark Notification As Read

## SQL Query

```sql
UPDATE notifications
SET is_read = TRUE,
    updated_at = CURRENT_TIMESTAMP
WHERE id = 'notif_101';
```

---

# 5. Mark All Notifications As Read

## SQL Query

```sql
UPDATE notifications
SET is_read = TRUE,
    updated_at = CURRENT_TIMESTAMP
WHERE user_id = 'user_501';
```

---

# 6. Delete Notification

## SQL Query

```sql
DELETE FROM notifications
WHERE id = 'notif_101';
```

---

# 7. Get Unread Notification Count

## SQL Query

```sql
SELECT COUNT(*) AS unread_count
FROM notifications
WHERE user_id = 'user_501'
AND is_read = FALSE;
```

---

# NoSQL Alternative

## MongoDB Schema Example

```json
{
  "_id": "notif_101",
  "userId": "user_501",
  "title": "Payment Successful",
  "message": "Your payment was successful.",
  "type": "payment",
  "priority": "high",
  "isRead": false,
  "createdAt": "2026-05-18T10:30:00Z"
}
```

---

# Why SQL Preferred Over NoSQL

| Feature | PostgreSQL | MongoDB |
|---|---|---|
| ACID Transactions | Yes | Limited |
| Structured Schema | Strong | Flexible |
| Complex Queries | Excellent | Moderate |
| Data Consistency | High | Medium |
| Relational Support | Excellent | Weak |

---

# Scalability Recommendations

- Use Redis for caching
- Implement pagination
- Use Kafka/RabbitMQ for event processing
- Apply database sharding for huge datasets
- Archive old records periodically
- Monitor DB performance regularly

---