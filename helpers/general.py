import os
import zipfile
from io import BytesIO, StringIO
from fastapi.responses import StreamingResponse

zip_subdir = ""

def zipfiles(filenames, zip_name):
    zip_io = BytesIO()
    with zipfile.ZipFile(zip_io, mode='w', compression=zipfile.ZIP_DEFLATED) as temp_zip:
        for fpath in filenames:
            # Calculate path for file in zip
            fdir, fname = os.path.split(fpath)
            zip_path = os.path.join(zip_subdir, fname)
            # Add file, at correct path
            temp_zip.write(fpath, zip_path)
    return StreamingResponse( 
        iter([zip_io.getvalue()]), 
        media_type="application/x-zip-compressed", 
        headers = { "Content-Disposition": f"attachment; filename={zip_name}.zip"}
    )
