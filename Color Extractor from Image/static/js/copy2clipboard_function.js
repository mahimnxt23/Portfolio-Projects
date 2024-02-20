function copyToClipboard(text) {
        // Create a temporary input element
        var tempInput = document.createElement("input");

        // Set its value to the text to be copied
        tempInput.value = text;

        // Append the input element to the body
        document.body.appendChild(tempInput);

        // Select the text inside the input element
        tempInput.select();

        // Copy the selected text to the clipboard
        document.execCommand("copy");

        // Remove the temporary input element
        document.body.removeChild(tempInput);

        // Show an alert or any other feedback to the user
        alert("HEX code copied to clipboard!");
    }
