edge = edge = {};


edge.domFactory = (() => {

    let newElement = (tag, options = {}) => {

        let element = document.createElement(tag);

        if (options.text) {

            let textNode = document.createTextNode(options.text);

            element.appendChild(textNode);

        }

        if (options.classes) {

            if (typeof options.classes === 'string') {

                element.className = options.classes;

            } else if (typeof options.classes === 'object') {

                for (let i = 0; i < options.classes.length; i++) {

                    element.classList.add(options.classes[i]);

                }

            }

        }

        if (options.attrs) {

            for (let key in options.attrs) {

                if (options.attrs.hasOwnProperty(key)) {

                    element.setAttribute(key, options.attrs[key]);

                }

            }

        }

        if (options.children) {

            for (let i = 0; i < options.children.length; i++) {

                if (options.children[i] instanceof HTMLElement) {

                    element.appendChild(options.children[i]);

                }

            }

        }

        return element;

    };


    let newNode = (data) => {

        return document.createTextNode(data);

    };


    return {
        newElement,
        newNode
    }

})();
