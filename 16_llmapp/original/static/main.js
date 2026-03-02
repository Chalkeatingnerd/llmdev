window.onload = function() {
    const chatBox = document.getElementById('chat-box');
    const textarea = document.getElementById('user-input');
    const form = document.getElementById('chat-form');

    chatBox.scrollTop = chatBox.scrollHeight;

    textarea.addEventListener('keydown', function(e) {
        if (e.ctrlKey && e.key === 'Enter') {
            e.preventDefault();
            form.submit();
        }
    });
};