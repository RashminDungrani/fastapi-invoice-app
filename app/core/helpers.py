# import os
# import uuid

# import aiofiles
# from fastapi import HTTPException, UploadFile


# async def handle_file_upload(
#     dir_location: str,
#     file: UploadFile,
#     supported_types: list[str] = ["image/jpeg", "image/jpg", "image/png"],
#     invalid_error_msg="Only .jpeg or .png  files allowed",
# ) -> str:
#     _, ext = os.path.splitext(file.filename)
#     if not ext:
#         ext = ".jpg"

#     if not os.path.exists(dir_location):
#         os.makedirs(dir_location)

#     if file.content_type not in supported_types:
#         raise HTTPException(status_code=406, detail=invalid_error_msg)

#     file_name = f"{uuid.uuid4().hex}{ext}"

#     async with aiofiles.open(os.path.join(dir_location, file_name), "wb") as out_file:
#         while content := await file.read(1024):  # async read chunk
#             await out_file.write(content)  # async write chunk

#     return file_name
