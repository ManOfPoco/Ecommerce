const urlParams = new URLSearchParams(window.location.search);
function handleOrderingChange(ordering) {
    urlParams.set('ordering', ordering);
    const newUrl = window.location.pathname + '?' + urlParams.toString();

    window.location.href = newUrl;
}

// select corrent order option if user chose any
$('#ordering').on('change', function (e) {
    handleOrderingChange(this.value)
});

// select correct ordering
const select = document.getElementById('ordering')
if (select && urlParams.has('ordering')) {
    for (option of select) {
        if (urlParams.get('ordering') === option.value) {
            option.selected = true;
        }
    }
}


// ajax create new wish list request
$('#create-list').on('submit', function (e) {
    let form = $(this)
    $.ajax({
        type: "POST",
        url: window.location.href,
        data: form.serialize(),
        success: function (response) {
            location.reload();
        },
        error: function (response) {
            form.find('.modal-messages').html('<div class="alert alert-danger" id="usernameError">Something went wrong</div>')
        }
    });
    return false;
});


// ajax edit wish list request
$('#edit-wish-list').on('submit', function (e) {
    let form = $(this)
    if ($(this).find('input[type=checkbox]').is(":checked") === false && $(this).find(':submit').data('default') === 'True') {
        form.find('.modal-messages').html("<div class='alert alert-danger m-0' id='default-error'>You can't delete default wish list</div>")
        return false
    };

    $.ajax({
        type: "POST",
        url: window.location.href,
        data: form.serialize(),
        success: function (response) {
            let oldslug = window.location.pathname.split('/').slice(-1)[0];
            history.replaceState(oldslug, "", response.slug);
            location.reload();
        },
        error: function (response) {
            form.find('.modal-messages').html('<div class="alert alert-danger" id="usernameError">Something went wrong</div>')
        }
    });
    return false;
});

// ajax request for item deletion from the wish list
$('.items-deletion-form').on('submit', function (e) {
    let form = $(this)

    $.ajax({
        type: "POST",
        url: window.location.href,
        data: form.serialize() + `&item_deletion=True`,
        success: function (response) {
            location.reload();
        },
        error: function (response) {
            form.find('.modal-messages').html('<div class="alert alert-danger" id="usernameError">Something went wrong</div>')
        }
    });
    return false;
});

// ajax request for wishlist deletion with check if user is trying to delete default wish list
$('#wish-list-delete').on('submit', function (e) {
    let form = $(this)
    if ($(this).find(':submit').data('default') === 'True') {
        form.find('.modal-messages').html("<div class='alert alert-danger m-0' id='default-error'>You can't delete default wish list</div>")
        return false
    };

    $.ajax({
        type: "POST",
        url: window.location.href,
        data: form.serialize() + '&wishlist_deletion=True',
        success: function (response) {
            let oldslug = window.location.pathname.split('/').slice(-1)[0];
            history.replaceState(oldslug, "", response.slug);
            location.reload();
        },
        error: function (response) {
            form.find('.modal-messages').html('<div class="alert alert-danger" id="usernameError">Something went wrong</div>')
        }
    });
    return false;
});