const video = document.getElementById('webcam');
const canvas = document.getElementById('overlay'); // Use the existing canvas
const context = canvas.getContext('2d');

// Prompt user for permission to use the webcam and display the video stream
if (navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(function (stream) {
            video.srcObject = stream;
        })
        .catch(function (error) {
            console.log("Something went wrong accessing the webcam!", error);
        });
}

// Function to capture frame and send it to the server
function captureAndSendFrame() {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    
    canvas.toBlob(blob => {
        const formData = new FormData();
        formData.append('image', blob);
        
        fetch('http://localhost:5000/detect', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            displayDetections(data.detections);
        })
        .catch(error => {
            console.error('Error during detection:', error);
        });
    });
}

// Call this function periodically
setInterval(captureAndSendFrame, 300); // Adjust interval as needed

function displayDetections(detections) {
    detections.forEach(detection => {
        const {xmin, ymin, xmax, ymax, name, confidence} = detection;
        console.log('confidence: ', confidence);
        // Draw the bounding box
        context.strokeStyle = '#00FF00'; // Green color for bounding box
        context.lineWidth = 4;
        context.strokeRect(xmin, ymin, xmax - xmin, ymax - ymin);

        // Draw the label
        context.fillStyle = '#00FF00'; // Green color for text
        context.font = '18px Arial';
        context.fillText(`${name} (${Math.round(confidence * 100)}%)`, xmin, ymin - 10);
    });
}
