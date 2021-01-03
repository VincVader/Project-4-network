const likeForm = document.querySelectorAll('like-form')
const likeUser = document.querySelectorAll('like-user')
const likePost = document.querySelectorAll('like-post')
const likeIcon = document.querySelectorAll('.like');
const likes = document.querySelectorAll('.like-count');

const followers = document.getElementById('followers')
const following = document.getElementById('following')
const follow = document.querySelector('.follow-btn');





if (follow) {
    let followUser = follow.dataset.user
    const followCount = async () => {
        await fetch(`/follow/${followUser}`, {
                method: "GET"
            })
            .then(response => response.json())
            .then(data => {
                follow.innerHTML = data.follow;
                followers.innerHTML = `Followers: ${data.followers}`;
                following.innerHTML = `Following: ${data.following}`;
            });
    };
    setTimeout(() => {
        followCount();
    }, 100);

    follow.addEventListener('click', () => {
        fetch(`/follow/${followUser}`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
            })
            .then(response => response.json())
            .then(result => {
                console.log(result)
                if (follow.classList.contains('followed')) {
                    follow.classList.remove('followed');
                    follow.innerHTML = 'Unfollow'
                } else {
                    follow.innerHTML = 'Follow'
                    follow.classList.add('followed');
                };
            });
        setTimeout(() => {
            followCount();
        }, 100);
    });
};

const likeCounter = async (likeData, item) => {
    await fetch(`/liked/${likeData}`, {
            method: "GET"
        })
        .then(response => response.json())
        .then(data => {
            item.innerHTML = data.data;
        });
};

let items = [];
likes.forEach(count => {
    items.push(count)
    likeCounter(count.dataset.post, count);
});

likeIcon.forEach((like, index) => {
    if (like.dataset.liked === 'True') {
        like.style.color = 'red';
        like.classList.add('liked');
    } else {
        like.style.color = 'grey';
        like.classList.remove('liked');
    };

    like.addEventListener('click', () => {
        if (like.classList.contains('liked')) {
            like.style.color = 'grey';
            like.classList.remove('liked');

            fetch('/liked', {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken
                    },
                    body: JSON.stringify({
                        post: like.dataset.post,
                        user: like.dataset.user,
                        liked: true
                    })
                })
                .then(response => response.json())
                .then(result => {
                    console.log(result)

                })
            setTimeout(() => {
                likeCounter(items[index].dataset.post, items[index]);
            }, 100);
        } else {

            like.classList.add('liked');
            like.style.color = 'red';

            fetch('/liked', {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken
                    },
                    body: JSON.stringify({
                        post: like.dataset.post,
                        user: like.dataset.user,
                        liked: false
                    })
                })
                .then(response => response.json())
                .then(result => {
                    console.log(result)
                })
            setTimeout(() => {
                likeCounter(items[index].dataset.post, items[index]);
            }, 100);

        };
    });
})