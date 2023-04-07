function ratingCreation(id, rating) {
    $(function () {
        $('#' + id).rateYo({
            rating: rating,
            readOnly: true,
            starWidth: "20px"
        });
    });
}