# Stage 1

# Notification System REST API Design

## Base URL

```http
https://api.example.com/api/v1
```

---

# Authentication Headers

```http
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json
Accept: application/json
```

---

# Core Actions Supported

1. Create Notification
2. Get All Notifications
3. Get Notification By ID
4. Mark Notification As Read
5. Mark All Notifications As Read
6. Delete Notification
7. Get Unread Notification Count
8. Real-Time Notification Delivery

---

# Notification Schema

```json
{
  "id": "notif_101",
  "userId": "user_501",
  "title": "Payment Successful",
  "message": "Your payment of ₹1200 was successful.",
  "type": "payment",
  "priority": "high",
  "isRead": false,
  "createdAt": "2026-05-18T10:30:00Z",
  "updatedAt": "2026-05-18T10:30:00Z"
}
```

---

# 1. Create Notification

## Endpoint

```http
POST /notifications
```

## Request Headers

```http
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json
```

## Request Body

```json
{
  "userId": "user_501",
  "title": "Payment Successful",
  "message": "Your payment of ₹1200 was successful.",
  "type": "payment",
  "priority": "high"
}
```

## Success Response

### Status

```http
201 Created
```

### Response Body

```json
{
  "success": true,
  "message": "Notification created successfully",
  "data": {
    "id": "notif_101",
    "userId": "user_501",
    "title": "Payment Successful",
    "message": "Your payment of ₹1200 was successful.",
    "type": "payment",
    "priority": "high",
    "isRead": false,
    "createdAt": "2026-05-18T10:30:00Z"
  }
}
```

---

# 2. Get All Notifications

## Endpoint

```http
GET /notifications
```

## Query Parameters

```http
?page=1&limit=10&isRead=false
```

## Request Headers

```http
Authorization: Bearer <JWT_TOKEN>
```

## Success Response

### Status

```http
200 OK
```

### Response Body

```json
{
  "success": true,
  "total": 2,
  "page": 1,
  "limit": 10,
  "data": [
    {
      "id": "notif_101",
      "title": "Payment Successful",
      "message": "Your payment of ₹1200 was successful.",
      "type": "payment",
      "priority": "high",
      "isRead": false,
      "createdAt": "2026-05-18T10:30:00Z"
    },
    {
      "id": "notif_102",
      "title": "New Login Detected",
      "message": "Your account logged in from a new device.",
      "type": "security",
      "priority": "medium",
      "isRead": true,
      "createdAt": "2026-05-18T09:00:00Z"
    }
  ]
}
```

---

# 3. Get Notification By ID

## Endpoint

```http
GET /notifications/{notificationId}
```

## Example

```http
GET /notifications/notif_101
```

## Success Response

### Status

```http
200 OK
```

### Response Body

```json
{
  "success": true,
  "data": {
    "id": "notif_101",
    "title": "Payment Successful",
    "message": "Your payment of ₹1200 was successful.",
    "type": "payment",
    "priority": "high",
    "isRead": false,
    "createdAt": "2026-05-18T10:30:00Z"
  }
}
```

---

# 4. Mark Notification As Read

## Endpoint

```http
PATCH /notifications/{notificationId}/read
```

## Example

```http
PATCH /notifications/notif_101/read
```

## Request Body

```json
{
  "isRead": true
}
```

## Success Response

### Status

```http
200 OK
```

### Response Body

```json
{
  "success": true,
  "message": "Notification marked as read"
}
```

---

# 5. Mark All Notifications As Read

## Endpoint

```http
PATCH /notifications/read-all
```

## Success Response

### Status

```http
200 OK
```

### Response Body

```json
{
  "success": true,
  "message": "All notifications marked as read"
}
```

---

# 6. Delete Notification

## Endpoint

```http
DELETE /notifications/{notificationId}
```

## Example

```http
DELETE /notifications/notif_101
```

## Success Response

### Status

```http
200 OK
```

### Response Body

```json
{
  "success": true,
  "message": "Notification deleted successfully"
}
```

---

# 7. Get Unread Notification Count

## Endpoint

```http
GET /notifications/unread/count
```

## Success Response

### Status

```http
200 OK
```

### Response Body

```json
{
  "success": true,
  "unreadCount": 5
}
```

---

# Error Response Structure

## Example

### Status

```http
401 Unauthorized
```

### Response Body

```json
{
  "success": false,
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Invalid authorization token"
  }
}
```

---

# Real-Time Notification Mechanism

## WebSocket Connection

```http
wss://api.example.com/ws/notifications
```

## WebSocket Authentication Header

```http
Authorization: Bearer <JWT_TOKEN>
```

## Real-Time Notification Event Payload

```json
{
  "event": "NEW_NOTIFICATION",
  "data": {
    "id": "notif_201",
    "title": "Order Shipped",
    "message": "Your order has been shipped successfully.",
    "type": "order",
    "priority": "medium",
    "isRead": false,
    "createdAt": "2026-05-18T11:00:00Z"
  }
}
```

---

# Recommended Notification Types

```json
[
  "payment",
  "security",
  "order",
  "promotion",
  "system",
  "message"
]
```

---

# Recommended Priority Levels

```json
[
  "low",
  "medium",
  "high"
]
```

---

# REST API Naming Conventions

| Method | Purpose |
|--------|----------|
| GET | Fetch Data |
| POST | Create Resource |
| PATCH | Update Resource |
| DELETE | Remove Resource |

---

# Security Recommendations

- Use JWT Authentication
- Validate Request Payloads
- Apply Rate Limiting
- Encrypt WebSocket Connections
- Log Notification Activities
- Prevent Unauthorized Access

---