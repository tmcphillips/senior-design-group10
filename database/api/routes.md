# api/v1/save/

### Request Types(s)
+ POST

### Request Body
NOTE:: recon json key has been removed from previous versions
```
{
    username: *String*
    title: *String*
    description: *String*
    model: *String*
    modelChecksum: *String*
    graph: *String*
    tags: [ *String* ]
    scripts: [
        { 
            name: *String*
            content: *String*
            checksum: *String*
        }
    ]
    files: [
        {
            name: *String*
            uri: *String*
            size: *Integer*
            checksum: *String*
            lastModified: *String*
        }
    ]
    programBlock: [
        {
            id: *Integer*
            inProgramBlock: *Integer* or *NULL*
            name: *String*
            qualifiedName: *String*
        }
    ]
    data: [
        {
            id: *Integer*
            inProgramBlock: *Integer* or *NULL*
            name: *String*
            qualifiedName: *String*
        }
    ]
    port: [
        {
            id: *Integer*
            onProgramBlock: *Integer*
            data: *Integer*
            name: *String*
            qualifiedName: *String*
            alias: *String* or *NULL*
            uriTemplate: *String* or *NULL*
            inPort: *Bool*
            outPort: *Bool*
        }
    ]
    channel: [
        {
            id: *Integer*
            outPort: *Integer*
            inPort: *Integer*
            data: *Integer*
            isInflow: *Bool*
            isOutflow: *Bool*
        }
    ]
    uriVariable: [ 
        {
            id: *Integer*
            port: *Integer*
            name: *String*
        }
    ]
    resource: [ 
        {
            id: *Integer*
            data: *Integer*
            uri: *String*
        } 
    ]
    uriVariableValue: [
        {
            uriVariable: *Integer*
            resource: *Integer*
            value: *String*
        }
    ]
}
```

### Response Body
```
{
    workflowId: *Integer*
    versionNumber: *Integer*
    runNumber: *Integer*
}
```

# api/v1/save/{workflow_id:int}/

### Request Types(s)
+ POST

### Request Body

Request body is identical to that of `api/v1/save/`

### Response Body
```
{
    workflowId: *Integer*
    versionNumber: *Integer*
    runNumber: *Integer*
    newVersion: *Bool*
}
```
