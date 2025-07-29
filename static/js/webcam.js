const WebcamManager = {
  videoElement: null,
  stream: null,

  init: function(videoId) {
    this.videoElement = document.getElementById(videoId);
    return this.startCamera();
  },

  startCamera: async function() {
    try {
      this.stream = await navigator.mediaDevices.getUserMedia({ video: true });
      this.videoElement.srcObject = this.stream;
    } catch (error) {
      console.error("Camera error:", error);
    }
  },

  captureImage: function() {
    const canvas = document.createElement("canvas");
    canvas.width = this.videoElement.videoWidth;
    canvas.height = this.videoElement.videoHeight;
    canvas.getContext("2d").drawImage(this.videoElement, 0, 0);
    return canvas.toDataURL("image/jpeg");
  }
};

document.addEventListener("DOMContentLoaded", () => {
  const video = document.getElementById("video");
  if (video) WebcamManager.init("video");
});
