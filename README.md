# API Documentation
## 1. Upload Video Endpoint
URL:
POST /upload

Description:
Allows clients to upload binary video files to the server.

## Request Headers:

## X-Filename: <filename>: The name of the file being uploaded.
### Request Body:

Binary data of the video file being uploaded.
Response:

`200 OK: If the file is uploaded successfully.`
```json
{
  "success": "File uploaded successfully"
}
```

`400 Bad Request: If the X-Filename header is missing.`
```json
{
  "error": "Missing filename header"
}
```

`413 Payload Too Large: If the uploaded file exceeds the maximum allowed size.`

```json
{
  "error": "File size exceeds the limit"
}
```

### Example:
```sh
curl -X POST -H "X-Filename: example.mp4" --data-binary @example.mp4 https://chrome-extension-0ez9.onrender.com/upload
```

## 2. Get Video Endpoint
URL:
GET /videos/<filename>

## Description:
Allows clients to request and stream the uploaded video files from the server.

## Parameters:

## filename: The name of the file to be fetched (including file extension).
Response:

## 200 OK: If the file is fetched successfully. The body will contain binary data of the video file.
## 404 Not Found: If the file with the given filename is not found.

```json
{
  "error": "File not found"
}
```
## Example:

```sh
curl -O https://chrome-extension-0ez9.onrender.com/videos/filename.mp4
```

## 3. List Videos Endpoint
URL:
GET /

## Description:
Retrieves a list of all uploaded videos on the server.

## Response:

## 200 OK: If the request is successful. The body will contain an HTML unordered list with links to the uploaded videos.
## 500 Internal Server Error: If there is any unexpected error.
```json
{
  "error": "Description of the error"
}
```