// // -------------------------------------------------- WORKING(THEME TOGGLING) - INDEXMF


// Theme Toggle Elements
const themeToggle = document.getElementById('themeToggle');
const themeIcon = document.getElementById('themeIcon');

// Check the current theme (default to dark)
const currentTheme = localStorage.getItem('theme') || 'dark';
document.body.setAttribute('data-theme', currentTheme);
themeToggle.checked = currentTheme === 'light';
updateThemeUI(currentTheme);

// Theme Toggle Event
themeToggle.addEventListener('change', () => {
    const newTheme = themeToggle.checked ? 'light' : 'dark';
    document.body.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeUI(newTheme);
});

// Update UI on Theme Change
function updateThemeUI(theme) {
    themeIcon.classList.remove('fa-sun', 'fa-moon');
    themeIcon.classList.add(theme === 'light' ? 'fa-sun' : 'fa-moon');
    themeIcon.classList.add('active'); // Rotation Animation
    setTimeout(() => themeIcon.classList.remove('active'), 500);
}

// File Upload
document.getElementById('fileInput').addEventListener('change', function () {
    const fileName = this.files[0]?.name;
    document.getElementById('status').textContent = `Selected: ${fileName}`;
});

// Predict Function
document.getElementById('predictBtn').addEventListener('click', function () {
    const fileInput = document.getElementById('fileInput');

    if (!fileInput.files[0]) {
        alert('Please select a video first!');
        return;
    }

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    fetch('/upload', { method: 'POST', body: formData })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                document.getElementById('videoSource').src = `/video/${data.filename}`;
                document.getElementById('videoPlayer').load();
                predictVideo(data.filename);
            }
        });
});

function predictVideo(filename) {
    const predictionText = document.getElementById('prediction');
    predictionText.textContent = 'Predicting...';
    predictionText.className = "";

    fetch('/predict', {
        method: 'POST',
        body: JSON.stringify({ filename }),
        headers: { 'Content-Type': 'application/json' }
    })
        .then(response => response.json())
        .then(data => {
            predictionText.textContent = data.prediction === 'Fight' ? 'Violence Detected' : 'No Violence Detected';;
            predictionText.className = data.prediction === 'Fight' ? 'fight' : 'no-fight';
        });
}




// // Theme Toggle Elements
// const themeToggle = document.getElementById('themeToggle');
// const themeIcon = document.getElementById('themeIcon');

// // Check the current theme (default to dark)
// const currentTheme = localStorage.getItem('theme') || 'dark';
// document.body.setAttribute('data-theme', currentTheme);
// themeToggle.checked = currentTheme === 'light';
// updateThemeUI(currentTheme);

// // Theme Toggle Event
// themeToggle.addEventListener('change', () => {
//     const newTheme = themeToggle.checked ? 'light' : 'dark';
//     document.body.setAttribute('data-theme', newTheme);
//     localStorage.setItem('theme', newTheme);
//     updateThemeUI(newTheme);
// });

// // Update UI on Theme Change
// function updateThemeUI(theme) {
//     themeIcon.classList.remove('fa-sun', 'fa-moon');
//     themeIcon.classList.add(theme === 'light' ? 'fa-sun' : 'fa-moon');
//     themeIcon.classList.add('active'); // Rotation Animation
//     setTimeout(() => themeIcon.classList.remove('active'), 500);
// }

// // File Upload
// document.getElementById('fileInput').addEventListener('change', function () {
//     const fileName = this.files[0]?.name;
//     document.getElementById('status').textContent = `Selected: ${fileName}`;
// });

// // Predict Function
// document.getElementById('predictBtn').addEventListener('click', function () {
//     const fileInput = document.getElementById('fileInput');

//     if (!fileInput.files[0]) {
//         alert('Please select a video first!');
//         return;
//     }

//     const formData = new FormData();
//     formData.append('file', fileInput.files[0]);

//     fetch('/upload', { method: 'POST', body: formData })
//         .then(response => response.json())
//         .then(data => {
//             if (data.error) {
//                 alert(data.error);
//             } else {
//                 const fileExtension = data.filename.split('.').pop().toLowerCase();
//                 if (fileExtension === 'avi') {
//                     document.getElementById('aviSource').src = `/video/${data.filename}`;
//                     document.getElementById('videoPlayer').load();
//                     predictVideo(data.filename);
//                 } else {
//                     document.getElementById('videoSource').src = `/video/${data.filename}`;
//                     document.getElementById('videoPlayer').load();
//                     predictVideo(data.filename);
//                 }
//             }
//         });
// });

// function predictVideo(filename) {
//     const predictionText = document.getElementById('prediction');
//     predictionText.textContent = 'Predicting...';

//     fetch('/predict', {
//         method: 'POST',
//         body: JSON.stringify({ filename }),
//         headers: { 'Content-Type': 'application/json' }
//     })
//         .then(response => response.json())
//         .then(data => {
//             predictionText.textContent = data.prediction;
//             predictionText.className = data.prediction === 'Fight' ? 'fight' : 'no-fight';
//         });
// }
