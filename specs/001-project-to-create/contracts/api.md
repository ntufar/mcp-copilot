# API Contracts

## Endpoints

### 1. List Directory Contents
```http
GET /api/v1/workspace/{workspaceId}/list
Query params:
  - path: string (relative path, default: "/")
  - recursive: boolean (default: false)
  - includeHidden: boolean (default: false)

Response (200 OK):
{
  "entries": [
    {
      "name": string,
      "path": string,
      "type": "file" | "directory",
      "size": number,
      "modified": string (ISO date),
      "permissions": string
    }
  ],
  "metadata": {
    "totalEntries": number,
    "hasMore": boolean
  }
}

Errors:
- 403: Access denied
- 404: Path not found
- 429: Rate limit exceeded
```

### 2. Read File Contents
```http
GET /api/v1/workspace/{workspaceId}/read
Query params:
  - path: string (relative path)
  - encoding: string (default: "utf-8")
  - maxSize: number (optional, override default limit)

Response (200 OK):
{
  "content": string (base64 for binary),
  "metadata": {
    "size": number,
    "encoding": string,
    "mimeType": string,
    "modified": string (ISO date)
  }
}

Errors:
- 403: Access denied
- 404: File not found
- 413: File too large
- 429: Rate limit exceeded
```

### 3. Workspace Management
```http
POST /api/v1/workspace
Request:
{
  "rootPath": string,
  "accessRules": [
    {
      "pattern": string,
      "permission": "read" | "list" | "none"
    }
  ]
}

Response (201 Created):
{
  "workspaceId": string,
  "status": "active",
  "created": string (ISO date)
}

Errors:
- 400: Invalid configuration
- 403: Unauthorized
```

### 4. Client Authentication
```http
POST /api/v1/auth
Request:
{
  "provider": string,
  "apiKey": string,
  "clientId": string
}

Response (200 OK):
{
  "token": string,
  "expires": string (ISO date),
  "permissions": [
    {
      "workspace": string,
      "access": "read" | "list" | "none"
    }
  ]
}

Errors:
- 401: Invalid credentials
- 403: Unauthorized provider
```

## Common Headers
```http
Request:
- Authorization: Bearer <token>
- X-Client-ID: <client_id>

Response:
- X-RateLimit-Remaining: number
- X-RateLimit-Reset: number (unix timestamp)
```

## Test Cases

### Security
1. Test access control enforcement
2. Verify path traversal prevention
3. Validate rate limiting
4. Check file size restrictions

### Functionality
1. List directories with various filters
2. Read files with different encodings
3. Handle workspace configuration
4. Manage client authentication

### Edge Cases
1. Handle concurrent access
2. Process large directories
3. Manage file system changes
4. Handle network interruptions