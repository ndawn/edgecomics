'use strict';


let parser = (() => {

    let mode = null;
    let releaseDate = null;
    let session = null;
    let queue = null;
    let queueLength = null;
    let threads = 10;
    let done = false;
    let dummy = false;


    let coversDownloadPoll = () => {

        if (queue.length) {

            let currentId = queue.pop();
            let xhr = new XMLHttpRequest();

            xhr.open('GET', '/previews/postparse/?mode=' + mode + '&id=' + currentId, true);

            xhr.onreadystatechange = () => {

                if (xhr.readyState === 4) {

                    if (xhr.status === 200) {

                        parserControls.fillItem(JSON.parse(xhr.responseText));

                    }

                    parserControls.updateProgress(queueLength - queue.length, queueLength);

                    coversDownloadPoll();

                }

            };

            xhr.send();

        } else {

            if (!done) {

                done = true;

                getPrice();

            }

        }

    };


    let startParse = (mode, relDate) => {

        let xhr = new XMLHttpRequest();

        parserControls.setLoadState('counting');

        xhr.open('GET', '/previews/parse/?mode=' + mode + (relDate ? '&release_date=' + relDate : ''));

        xhr.onreadystatechange = () => {

            if (xhr.status == 200 && xhr.readyState == 4) {

                let response = JSON.parse(xhr.responseText);

                queue = response.entry_list;
                queueLength = queue.length;
                session = response.session;

                parserControls.updateProgress(0, 1);

                startDownloadPoll();

            }

        };

        xhr.send();

    };


    let startDownloadPoll = () => {

        if (!dummy) {

            parserControls.enableItem();

            for (let i = 0; i < threads; i++) {

                coversDownloadPoll();

            }

        } else {

            getPrice();

        }

    };


    let getPrice = () => {

        parserControls.enableLoader();
        parserControls.setPriceLink(mode, session);
        parserControls.setLoadState('done');

    };


    let addListeners = () => {

        parserControls.monthlyButton.addEventListener('click', event => {

            parserControls.weeklyButton.classList.remove('active');
            parserControls.monthlyButton.classList.add('active');
            mode = 'monthly';

        });

        parserControls.weeklyButton.addEventListener('click', event => {

            parserControls.monthlyButton.classList.remove('active');
            parserControls.weeklyButton.classList.add('active');
            mode = 'weekly';

        });

        parserControls.submitButton.addEventListener('click', event => {

            releaseDate = parserControls.releaseDateInput.value;

            parserControls.enableLoader();
            startParse(mode, releaseDate);

        });

    };


    let init = () => {

        addListeners();

    };


    return {
        init: init
    }

})();


document.addEventListener('DOMContentLoaded', event => {

    parser.init();

});
