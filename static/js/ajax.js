edge = edge || {};


edge.ajax = (url, method, json, callback) => {

    let xhr = new XMLHttpRequest();

    xhr.open(method, url, true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    xhr.onreadystatechange = () => {

        if (xhr.readyState === 4) {

            let response = JSON.parse(xhr.responseText);

            if (response.error !== undefined) {

                console.error(response.error);

            } else {

                if (callback !== undefined) {

                    console.log(response);

                    callback(response);

                }

            }

        }

    };

    xhr.send(
        json === undefined
            ? undefined
            : (
                typeof json === 'string'
                    ? json
                    : JSON.stringify(json)
            )
    );

};
