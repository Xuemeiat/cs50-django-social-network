

function getCookie(name){
    let cookieValue = null;

    if(document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';')

        for(let cookie of cookies) {
            cookie = cookie.trim();
            if(cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break
            }
        }
    }
    
    return cookieValue;
}

document.addEventListener("DOMContentLoaded", () => {
    const postsContainer = document.getElementById("posts-container");

    if (!postsContainer) return;
    
    postsContainer.addEventListener("click", (e) => {

        const editLink = e.target.closest(".edit-link");
        if(editLink) {
            e.preventDefault();
            handleEditClick(editLink);
        }

        const likePost = e.target.closest(".like-post");
        if (likePost) {
            e.preventDefault();
            handleLikePost(likePost);
        }
    })
});


// EDIT POST

function handleEditClick(editLink) {
 

   
    console.log("Edit clicked!");
    const postId = editLink.dataset.postId;
    console.log("Post Id: ", postId);
    const postDiv = document.querySelector(`#post-${postId}`);
    const contentElement = postDiv.querySelector('.post-content');

    // Save original content
    const originalContent = contentElement.innerText;
    

    // Replace content with textarea
    contentElement.innerHTML = `
        <textarea class="edit-textarea" rows="4" style="width: 100%;">${originalContent}</textarea>
        <br>
        <button class="save-btn">Save</button>
    `;

    editLink.style.display = 'none';

    //Add event listener do Save button
    const saveButton = postDiv.querySelector(".save-btn");

    saveButton.addEventListener("click", () => savePost(postId, postDiv, editLink));

    }


function savePost(postId, postDiv, editLink) {
    const newContent = postDiv.querySelector(".edit-textarea").value;
    console.log("New content:", newContent);

    fetch(`/edit-post/${postId}/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: JSON.stringify({
            content : newContent})
        
    })
//JSON returned by backend

    .then(response => response.json())
    .then(data => { 
        if(data.success) {
            postDiv.querySelector(".post-content").textContent = data.content;
            editLink.style.display = "inline";
            alert("Post updated successfully!");
            } else if(data.error){
                alert("Error: " + data.error);
            }
    })
    .catch(error =>{
        console.error("Fetch error:", error);
        alert("An unexpected error ocurred.")
    });

}

// LIKE POST
function handleLikePost(likePost){
    const postId = likePost.dataset.postId;
    console.log("like is clicked for post: ", postId);

    fetch(`/like/${postId}/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken")
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        const likesCounter = document.getElementById(`likes-${postId}`);
        likesCounter.textContent = '❤️' + data.likes;
        likePost.textContent = data.liked ? 'Unlike' : 'Like';   
    })

    
}
