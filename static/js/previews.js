'use strict';


let previews = (() => {

    let formBox = null;
    let loadingBox = null;
    let completeBox = null;

    let form = null;
    let datesBox = null;
    let msgLinkBox = null;
    let submitButton = null;
    let repeatButton = null;


    let showForm = () => {

        formBox.classList.remove('hidden');
        loadingBox.classList.add('hidden');
        completeBox.classList.add('hidden');

    };


    let showLoading = () => {

        formBox.classList.add('hidden');
        loadingBox.classList.remove('hidden');
        completeBox.classList.add('hidden');

    };


    let showComplete = () => {

        formBox.classList.add('hidden');
        loadingBox.classList.add('hidden');
        completeBox.classList.remove('hidden');

    };


    let addListeners = () => {

        submitButton.addEventListener('click', (event) => {

            if (form.group_id.value === '' || datesBox === null) {

                submitButton.setAttribute('disabled', '');
                submitButton.setAttribute('alt', 'Заполните все параметры')

            } else {

                showLoading();

                let xhr = new XMLHttpRequest();

                xhr.open('POST', '/previews/', true);

                xhr.onreadystatechange = (event) => {

                    if (xhr.readyState === 4 && xhr.status === 200) {

                        showComplete();

                    }

                };

                let data = new FormData();

                data.append('group_id', form.group_id.value);
                data.append('csrfmiddlewaretoken', form.csrfmiddlewaretoken.value);
                data.append('session', form.session.value);
                data.append('msg_link', form.msg_link.value);

                xhr.send(data);

            }

        });

        for (let group of document.querySelectorAll('.group-box')) {

            group.addEventListener('click', (event) => {

                for (let g of document.querySelectorAll('.group-box')) {

                    g.classList.remove('selected');

                }

                group.classList.add('selected');
                form.group_id.value = group.dataset.id;

                if (datesBox !== null) {

                    submitButton.removeAttribute('disabled');
                    submitButton.removeAttribute('alt');

                }

            });

        }

        repeatButton.addEventListener('click', (event) => {

            showForm();

        });

    };


    let fill = () => {

        form = document.getElementById('form');
        formBox = document.getElementById('form-box');
        loadingBox = document.getElementById('loading-box');
        completeBox = document.getElementById('complete-box');
        datesBox = document.getElementById('dates-box');
        msgLinkBox = document.getElementById('msg-link-box');
        submitButton = document.getElementById('submit-button');
        repeatButton = document.getElementById('repeat-button');

    };


    let init = () => {

        fill();
        addListeners();

    };


    return {
        init
    };

})();


previews.init();
