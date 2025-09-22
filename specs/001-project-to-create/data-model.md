# Data Model

## Core Entities

### Workspace
- **Purpose**: Represents a root directory with access controls
- **Attributes**:
  * ID: Unique workspace identifier
  * Root Path: Absolute path to workspace root
  * Access Rules: List of path patterns (allow/deny)
  * Created At: Timestamp
  * Updated At: Timestamp
  * Status: Active/Inactive

### Directory
- **Purpose**: Represents a directory within a workspace
- **Attributes**:
  * Path: Relative path from workspace root
  * Parent: Reference to parent directory
  * Metadata: Last modified, permissions
  * Entry Count: Number of contained items
  * Type: Regular/Special

### File
- **Purpose**: Represents a file within the workspace
- **Attributes**:
  * Path: Relative path from workspace root
  * Size: File size in bytes
  * Metadata: Last modified, permissions, mime type
  * Hash: Content hash for caching/validation
  * Type: Text/Binary

### AccessControl
- **Purpose**: Defines access rules and permissions
- **Attributes**:
  * Resource Path: File/directory path pattern
  * Permissions: Read/List/None
  * Client ID: Associated LLM client
  * Conditions: Time-based or state-based restrictions

### LLMClient
- **Purpose**: Represents an authenticated LLM consumer
- **Attributes**:
  * ID: Unique client identifier
  * Type: Provider type (GitHub/OpenAI/Anthropic)
  * API Key: Authentication credentials
  * Rate Limits: Request quotas
  * Access Level: Permission level

### AuditLog
- **Purpose**: Records all file system operations
- **Attributes**:
  * Timestamp: Operation time
  * Client ID: Requesting client
  * Operation: Action performed
  * Resource Path: Affected resource
  * Status: Success/Failure
  * Error: Error details if failed
  * Metadata: Additional context

## Relationships
1. Workspace --contains--> Directory/File
2. Directory --contains--> Directory/File
3. AccessControl --applies-to--> Workspace
4. LLMClient --has--> AccessControl
5. AuditLog --references--> LLMClient, Resource

## Validation Rules
1. All paths must be relative to workspace root
2. File sizes must respect configured limits
3. Access rules are evaluated hierarchically
4. Client operations must respect rate limits
5. Binary files must be explicitly allowed

## Security Considerations
1. Paths must be normalized and validated
2. No symbolic link traversal outside workspace
3. File content must be scanned for sensitive data
4. Access rules are default-deny
5. All operations must be logged