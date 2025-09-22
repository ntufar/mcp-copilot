# MCP Server Quickstart Guide

## Overview
MCP Server provides secure directory browsing capabilities for Language Models (LLMs) like GitHub Copilot, ChatGPT, and Claude. This guide helps you get started with integrating and using the server.

## Features
- Secure workspace isolation
- Directory listing and file access
- Multi-LLM support
- Audit logging
- Rate limiting
- Access controls

## Integration Examples

### GitHub Copilot
```javascript
const workspace = await MCPServer.createWorkspace({
  rootPath: '/path/to/project',
  provider: 'github'
});

// List directory contents
const files = await workspace.list('/src');

// Read file contents
const content = await workspace.readFile('/src/main.js');
```

### OpenAI (ChatGPT)
```python
from mcp_server import Workspace

workspace = Workspace.create(
    root_path="/path/to/project",
    provider="openai"
)

# List directory contents
files = workspace.list("/src")

# Read file contents
content = workspace.read_file("/src/main.py")
```

### Anthropic (Claude)
```python
from mcp_server import Workspace

workspace = Workspace.create(
    root_path="/path/to/project",
    provider="anthropic"
)

# List directory contents
files = workspace.list("/src")

# Read file contents
content = workspace.read_file("/src/main.py")
```

## Security Best Practices
1. Always use workspace isolation
2. Configure strict access rules
3. Monitor audit logs
4. Set appropriate rate limits
5. Review file access patterns

## Configuration
```yaml
# config.yaml
server:
  port: 3000
  host: localhost

security:
  max_file_size: 10MB
  max_dir_entries: 1000
  rate_limit:
    requests_per_minute: 100
    concurrent_connections: 10

workspace:
  default_rules:
    - deny: "**/.env"
    - deny: "**/node_modules"
    - allow: "**/*"
```

## Getting Help
- Documentation: [docs/](link)
- Issues: [GitHub Issues](link)
- Security: [SECURITY.md](link)