# api/v1/save/

### Request Types(s)
+ POST

### Request Body
NOTE:: recon json key has been removed from previous versions
```
{
    username: String
    title: String
    description: String
    model: String
    modelChecksum: String
    graph: String
    tags: [ String ]
    scripts: [
        { 
            name: String
            content: String
            checksum: String
        }
    ]
    files: [
        {
            name: String
            uri: String
            size: Integer
            checksum: String
            lastModified: String
        }
    ]
    NOTE: Will these be sorted by program_block_id? Can we gurantee that a inProgramBlock has been created first?
    programBlock: [
        {
            programBlockId: Integer
            inProgramBlock: Integer or NULL
            name: String
            qualifiedName: String
        }
    ]
    data: [
        {
            dataId: Integer
            inProgramBlock: Integer or NULL
            name: String
            qualifiedName: String
        }
    ]
    port: [
        {
            portId: Integer
            inProgramBlock: Integer
            data: Integer
            name: String
            qualifiedName: String
            alias: String or NULL
            uriTemplate: String or NULL
            inPort: Bool
            outPort: Bool
        }
    ]
    channel: [
        {
            channelId: Integer
            outPort: Integer
            inPort: Integer
            data: Integer
            isInflow: Bool
            isOutflow: Bool
        }
    ]
    uriVariable: [ 
        {
            uriVariableId: Integer
            port: Integer
            name: String
        }
    ]
    resource: [ 
        {
            resourceId: Integer
            data: Integer
            uri: String
        } 
    ]
    uriVariableValue: [
        {
            uriVariableId: Integer
            resource: Integer
            value: String
        }
    ]
}
```

### Response Body
```
{
    workflowId: Integer
    versionNumber: Integer
    runNumber: Integer
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
    workflowId: Integer
    versionNumber: Integer
    runNumber: Integer
    newVersion: Bool
}
```
