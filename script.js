function fetchStatus() {
    $.get('/status', function(data) {
        let postsList = $('#posts');
        postsList.empty();
        data.posts.forEach(p => postsList.append(`<li>${p}</li>`));

        let votesList = $('#votes');
        votesList.empty();
        for (let user in data.votes) {
            votesList.append(`<li>${user} → ${data.votes[user]}</li>`);
        }

        $('#randomMessage').text(data.message);
    });
}

function addPost() {
    let content = $('#postContent').val();
    $.post('/post', {content: content}, function() {
        $('#postContent').val('');
        fetchStatus();
    });
}

function castVote() {
    let name = $('#voterName').val();
    let choice = $('#voteChoice').val();
    $.post('/vote', {name: name, choice: choice}, function() {
        $('#voteChoice').val('');
        fetchStatus();
    });
}

function sendMessage() {
    let content = $('#messageContent').val();
    $.post('/message', {content: content}, function() {
        $('#messageContent').val('');
        fetchStatus();
    });
}

setInterval(fetchStatus, 5000);
fetchStatus();
