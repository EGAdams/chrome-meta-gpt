```mermaid
sequenceDiagram
    participant AC as AccelerationController
    participant C as Converter
    participant S as Speedometer
    participant Config as Configuration

    AC->>Config: Retrieve speedometerScales configuration
    Config->>AC: Return {5, 10, 20, 40, 100}
    AC->>C: Convert raw acceleration values based on scale
    C->>AC: Return converted values
    AC->>S: Update speedometer with converted values
``````