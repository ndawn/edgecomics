let parserControls = (() => {

    let container = document.getElementById('container');
    let progressBar = document.getElementById('progress');
    let selectContainer = document.getElementById('select');
    let monthlyButton = document.getElementById('monthly');
    let weeklyButton = document.getElementById('weekly');
    let releaseDateInput = document.getElementById('release_date');
    let submitButton = document.getElementById('submit');
    let loadingContainer = document.getElementById('loading');
    let itemContainer = document.getElementById('item');
    let loadingStateText = document.getElementById('loading_state');
    let loadingAnimation = document.getElementById('loading_animation');
    let doneMarker = document.getElementById('done_marker');
    let priceButton = document.getElementById('price');
    let itemCover = document.getElementById('item_cover');
    let itemTitle = document.getElementById('item_title');


    let enable = element => {

        element.classList.remove('disabled');

    };


    let disable = element => {

        element.classList.add('disabled');

    };


    let enableLoader = () => {

        disable(selectContainer);
        disable(itemContainer);
        setLoadState('waiting');
        enable(loadingContainer);

    };


    let setLoadState = state => {

        if (state == 'waiting') {

            loadingStateText.textContent = 'Идёт загрузка';
            disable(doneMarker);
            disable(priceButton);
            enable(loadingAnimation);

        } else if (state == 'counting') {

            loadingStateText.textContent = 'Идёт подсчёт объектов';
            disable(doneMarker);
            disable(priceButton);

        } else if (state == 'done') {

            loadingStateText.textContent = 'Загрузка завершена';
            disable(loadingAnimation);
            enable(doneMarker);
            enable(priceButton);

        }

    };


    let enableItem = () => {

        disable(selectContainer);
        disable(loadingContainer);
        enable(itemContainer);

    };


    let fillItem = params => {

        itemCover.src = params.cover;
        itemTitle.textContent = params.title;

    };


    let updateProgress = (loaded, overall) => {

        progressBar.style.width = container.offsetWidth * loaded / overall + 'px';

    };


    let setPriceLink = (mode, session) => {

        let xhr = new XMLHttpRequest();

        xhr.open('GET', '/previews/price/?mode=' + mode + '&session=' + session);

        xhr.onreadystatechange = () => {

            if (xhr.status == 200 && xhr.readyState == 4) {

                priceButton.href = JSON.parse(xhr.responseText).url;

            }

        };

        xhr.send();

    };


    return {
        container,
        progressBar,
        selectContainer,
        monthlyButton,
        weeklyButton,
        releaseDateInput,
        submitButton,
        loadingContainer,
        itemContainer,
        loadingStateText,
        loadingAnimation,
        doneMarker,
        priceButton,
        itemCover,
        itemTitle,

        enable,
        disable,
        enableLoader,
        setLoadState,
        enableItem,
        fillItem,
        updateProgress,
        setPriceLink,
    }

})();
