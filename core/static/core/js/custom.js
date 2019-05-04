{
const likeTrigger = document.querySelector('#like_action')
const icon = document.querySelector('#like-heart')

likeTrigger.addEventListener('click',(e) => {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
    e.preventDefault();
    const postId = likeTrigger.getAttribute('data-id')
    fetch('/likes/',{
        method:'post',
        headers:{
            "Content-type":"application/json",
            "X-CSRFToken": csrftoken
        },
        body: JSON.stringify({
            "post":postId
        })
    })
    .then(data => data.json())
    .then(payload => {
        console.log(payload)
        if(payload.code === 201) {
            icon.style.color = 'red'
        } else {
            console.log(payload.errors)
        }

    })
    .catch(console.log)
})
}