
    $(document).ready(function () {
        var updateCategoryUrl = "/update_category/";
        var deleteCategoryUrl = "/delete_category/";
        function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        const csrftoken = getCookie('csrftoken');

        // Setup AJAX with CSRF token
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });
        $('.category-item').hover(
            function () {
                $(this).find('.edit-category, .delete-category').removeClass('d-none');
            },
            function () {
                $(this).find('.edit-category, .delete-category').addClass('d-none');
            }
        );

        $('.edit-category').click(function () {
            var listItem = $(this).closest('.category-item');
            listItem.find('.category-name').addClass('d-none');
            listItem.find('.category-input').removeClass('d-none').focus();
        });

        $('.category-input').on('blur', function () {
            var input = $(this);
            var newName = input.val();
            var categoryId = input.closest('.category-item').data('id');

            $.ajax({
                url: updateCategoryUrl,
                method: 'POST',
                data: {
                    'id': categoryId,
                    'name': newName,
                    'csrfmiddlewaretoken': csrftoken
                },

                success: function () {
                    input.siblings('.category-name').text(newName).removeClass('d-none');
                    input.addClass('d-none');
                    console.log("Information updated")
                }

            });
        });

        $('.delete-category').click(function () {
            if (confirm('Are you sure you want to delete this category?')) {
                var listItem = $(this).closest('.category-item');
                var categoryId = listItem.data('id');
                $.ajax({
                    url: deleteCategoryUrl,
                    method: 'POST',
                    data: {
                        'id': categoryId,
                        'csrfmiddlewaretoken': csrftoken
                    },
                    success: function () {
                        listItem.remove();
                    }
                });
            }
        });
    });
