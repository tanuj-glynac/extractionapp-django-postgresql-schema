# extractionapp-django-postgresql-schema

This repository contains the Django models that mirror a PostgreSQL schema. The schema is divided into two main sections:

1. **Core Models** – These models include `Organization`, `User`, `Platform`, `Integration`, and `Employee`. They capture the main entities of the system.
2. **Extracted Data Models** – These models handle extracted data from various Microsoft 365 services, including calendar events, documents, emails, and Teams chats.

## Models Overview

- **Organization**: Represents an organization with details like name, industry, size, and additional information in JSON format.
- **User**: Captures user information, linked to an organization, with support for both password-based and OAuth-based authentication.
- **Platform**: Contains details of the communication platforms that the system integrates with.
- **Integration**: Stores integration details including tokens, scopes, and references to both the platform and organization.
- **Employee**: Represents employees within an organization.
- **MsCalendarEvent, MsDocument, MsEmail, TeamsChat**: These models store data extracted from Microsoft 365 services, with relationships to the core models for context and traceability.

## Usage

1. **Setup your Django project** if you haven't already.
2. **Create an app** (for example, `core`) and replace its `models.py` file with the content from this repository.
3. **Run migrations**:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
4. **Customize and extend** these models as needed for your project.

## License

This project is open-sourced for development and educational purposes.
