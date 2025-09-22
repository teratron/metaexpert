# Updated Data Model: MetaExpert Library Template Enhancement

## Entities

### TemplateFile
Represents the template.py file that serves as the starting point for all trading strategies.

**Attributes:**
- path: string - File path where the template is located
- content: string - The content of the template file
- version: string - Version of the template
- last_modified: datetime - When the template was last modified

**Relationships:**
- None (standalone entity)

### ConfigurationParameter
Represents a configuration parameter in the template.

**Attributes:**
- name: string - Name of the parameter
- description: string - Description of what the parameter does
- default_value: string - Default value of the parameter
- category: string - Category/group the parameter belongs to
- required: boolean - Whether the parameter is required
- env_var_name: string - Corresponding environment variable name
- cli_arg_name: string - Corresponding command-line argument name

**Relationships:**
- Belongs to TemplateFile (one-to-many)

### EventHandler
Represents an event handler function in the template.

**Attributes:**
- name: string - Name of the event handler function
- description: string - Description of when the handler is called
- parameters: list - List of parameters the handler accepts
- decorator: string - The decorator used to register the handler

**Relationships:**
- Belongs to TemplateFile (one-to-many)

### Exchange
Represents a supported exchange.

**Attributes:**
- name: string - Name of the exchange
- supported_features: list - List of features supported by the exchange
- api_documentation_url: string - URL to the exchange's API documentation
- requires_passphrase: boolean - Whether the exchange requires an API passphrase

**Relationships:**
- Referenced in TemplateFile configuration

### ConfigurationSource
Represents a source of configuration values.

**Attributes:**
- type: string - Type of configuration source (environment, cli, file, default)
- priority: int - Priority order for applying configuration values
- description: string - Description of the configuration source

**Relationships:**
- Used by ConfigurationParameter (many-to-many)

### StrategyParameter
Represents a strategy-specific parameter in the template.

**Attributes:**
- name: string - Name of the parameter
- description: string - Description of what the parameter does
- default_value: string - Default value of the parameter
- category: string - Category/group the parameter belongs to
- required: boolean - Whether the parameter is required

**Relationships:**
- Belongs to TemplateFile (one-to-many)