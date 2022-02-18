const closeAlertMessage = function () {
    const alertButtons = document.querySelectorAll('.alert__button');
    if (alertButtons) {
        alertButtons.forEach(btn => {
            btn.addEventListener("click", function () {
                const alertWrapper = btn.parentElement;
                alertWrapper.style.display = "none";
            })
        });
    }
}

const connectSearchWithPagination = function () {
    const searchForm = document.querySelector(".search-form");

    if (searchForm) {
        const pageButtons = document.querySelectorAll(".pagination__button");

        pageButtons.forEach(button => {
            button.addEventListener("click", (e) => {
                e.preventDefault();
                const pageNumber = button.dataset.page;
                searchForm.innerHTML += `<input type="text" name="page" value="${pageNumber}" hidden>`
                searchForm.submit();
            })
        });
    }
}

const removeTag = function () {
    const tags = document.querySelectorAll(".js-tag");

    tags.forEach(tag => {
        tag.addEventListener("click", (e) => {
            tagId = tag.dataset.tag;
            projectId = tag.dataset.project;

            const endpoint = `${window.location.protocol}//${window.location.hostname}/api/remove-tag/`;
            fetch(endpoint, {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    "tag": tagId,
                    "project": projectId
                }),
            }).then(response => response.json())

            tag.remove()
        })
    });
}

const showNavbarMenu = function () {
    const navButton = document.querySelector('.navbar__button');
    const navMenu = document.querySelector('.navbar__menu');
    let isnavMenuVisible = false;

    navButton.addEventListener("click", function () {
        if (!isnavMenuVisible) {
            navButton.classList.add("js-change");
            navMenu.classList.add("js-show");
            isnavMenuVisible = true;
        } else {
            navButton.classList.remove("js-change");
            navMenu.classList.remove("js-show");
            isnavMenuVisible = false;
        }
    });
}