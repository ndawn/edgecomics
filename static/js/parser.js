'use strict';


let parser = (() => {

    let mode = null;
    let releaseDate = null;
    let queue = null;
    let threads = 5;


    let coversDownloadPoll = () => {

        if (queue.length) {

            let currentId = queue.pop();
            let xhr = new XMLHttpRequest();

            xhr.open('GET', '/previews/postparse?mode=' + mode + '&id=' + currentId, true);

            xhr.onreadystatechange = () => {

                if (xhr.status == 200 && xhr.readyState == 4) {

                    parserControls.fillItem(JSON.parse(xhr.responseText));

                    coversDownloadPoll();

                }

            };

            xhr.send();

        } else {

            parserControls.enableLoader();
            parserControls.setLoadState('done');
            parserControls.setPriceLink(mode, releaseDate);

        }

    };


    let startParse = (mode, releaseDate) => {

        console.log('Starting parse');

        let xhr = new XMLHttpRequest();

        parserControls.setLoadState('counting');

        xhr.open('GET', '/previews/parse?mode=' + mode + (releaseDate ? '&release_date=' + releaseDate : ''));

        xhr.onreadystatechange = () => {

            if (xhr.status == 200 && xhr.readyState == 4) {

                let response = JSON.parse(xhr.responseText);

                queue = response.entry_list;
                releaseDate = response.release_date;

                parserControls.updateProgress(0, queue.length);

                startDownloadPoll();

            }

        };

        xhr.send();

    };


    let startDownloadPoll = () => {

        parserControls.enableItem();

        for (let i = 0; i < threads; i++) {

            coversDownloadPoll();

        }

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
