import { useState } from "react";

function Upload() {

  const [selectedFile, setSelectedFile] = useState(null);
  const handleUpload = () => {
    alert("Upload button clicked!");
  };

  return (
    <div>
      <h2>Upload PDF</h2>

      <input
        type="file"
        onChange={(e) => setSelectedFile(e.target.files[0])}
      />

      <button onClick={handleUpload}>
  Upload
</button>

      <p>{selectedFile?.name}</p>
    </div>
  );
}

export default Upload;