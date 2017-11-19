'use strict';


let edge = {
    domFactory: (() => {

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

    })(),


    filters: {
        rub: (value) => {

            return value + 'р.';

        },

        quantity: (value) => {

            return value + 'шт.';

        }
    },


    ajax: (url, method, json, callback) => {

        let xhr = new XMLHttpRequest();

        xhr.open(method, url, true);
        xhr.setRequestHeader('Content-Type', 'application/json');

        xhr.onreadystatechange = () => {

            if (xhr.readyState === 4) {

                let response = JSON.parse(xhr.responseText);

                if (callback !== undefined) {

                    callback(response);

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

    },


    api: (() => {

        let get = (callback) => {

            edge.ajax('/api/cart/', 'GET', undefined, callback);

        };


        let add = (itemId, callback) => {

            edge.ajax('/api/cart/add/', 'POST', {id: itemId}, callback);

        };


        let update = (cartItem, callback) => {

            edge.ajax('/api/cart/update/', 'POST', {id: cartItem.id, quantity: cartItem.quantity}, callback);

        };


        let remove = (cartItem, callback) => {

            edge.ajax('/api/cart/remove/', 'POST', {id: cartItem.id}, callback);

        };


        let clear = (callback) => {

            edge.ajax('/api/cart/clear/', 'POST', undefined, callback);

        };


        return {
            get,
            add,
            update,
            remove,
            clear
        }

    })(),


    cartDropdown: (() => {

        let toggleButton = null;
        let counter = null;
        let counterInner = null;
        let menu = null;
        let items = null;
        let overallNumber = null;
        let checkout = null;


        let buildItemElement = (element) => {

            let e = edge.domFactory.newElement;

            if (element === undefined) {

                return e('li', {
                    classes: ['cart_dropdown_item', 'cart_dropdown_item_empty'],
                    children: [e('h3', {text: 'Корзина пустая'})]
                });

            } else {

                let sumRub = edge.filters.rub(element.item.price * element.quantity);
                let quantity = edge.filters.quantity(element.quantity);

                let removeButton;

                return {element:
                    e('li', {
                        classes: 'cart_dropdown_item',
                        children: [
                            e('div', {
                                classes:'cart_dropdown_item_image',
                                attrs: {
                                    style: `background-image : url("${element.item.cover_list.thumb}")`
                                }
                            }),
                            e('div', {
                                classes: 'cart_dropdown_item_text',
                                children: [
                                    e('a', {
                                        classes: 'cart_dropdown_item_title',
                                        text: element.item.title,
                                        attrs: {
                                            href: `/item/${element.item.id}`
                                        }
                                    }),
                                    e('div', {
                                        classes: 'cart_dropdown_item_quantity',
                                        text: quantity
                                    }),
                                    e('div', {
                                        classes: 'cart_dropdown_item_overall',
                                        text: sumRub
                                    })
                                ]
                            }),
                            e('div', {
                                classes: 'cart_dropdown_item_remove',
                                children: [
                                    removeButton = e('a', {
                                        children: [e('span', {classes: ['fa', 'fa-times']})]
                                    })
                                ]
                            })
                        ]
                    }),
                    removeButton
                };

            }

        };


        let toggle = () => {

            menu.classList.toggle('hidden');

        };


        let clear = () => {

            while (items.firstChild) {

                items.removeChild(items.firstChild);

            }

        };


        let update = (itemList) => {

            clear();

            checkout.setAttribute('disabled', '');

            counter.textContent = itemList.length;
            counterInner.textContent = itemList.length;

            let overall = 0;

            if (itemList.length) {

                for (let i = 0; i < itemList.length; i++) {

                    let cartItem = itemList[i];

                    overall += cartItem.item.price * cartItem.quantity;

                    let item = buildItemElement(cartItem);

                    items.appendChild(item.element);

                    item.removeButton.addEventListener('click', (event) => {

                        edge.cart.remove(cartItem);

                    });

                }

                checkout.removeAttribute('disabled');

            } else {

                items.appendChild(buildItemElement());

            }

            overallNumber.textContent = edge.filters.rub(overall);

        };


        let init = () => {

            toggleButton = document.getElementById('cartDropdownToggle');
            counter = document.getElementById('cartDropdownCounter');
            counterInner = document.getElementById('cartDropdownCounterInner');
            menu = document.getElementById('cartDropdownMenu');
            items = document.getElementById('cartDropdownItems');
            overallNumber = document.getElementById('cartDropdownOverall');
            checkout = document.getElementById('cartDropdownCheckout');

            edge.cart.getCart().onChange((content) => {

                update(content);

            });

        };


        return {
            toggle,
            clear,
            update,
            init
        }

    })(),


    cart: (() => {

        let cart = (() => {

            let content = [];

            content.watchers = [];

            content.update = (newContent) => {

                newContent.watchers = content.watchers;
                newContent.update = content.update;
                newContent.onChange = content.onChange;

                content = newContent;

                for (let i = 0; i < content.watchers.length; i++) {

                    content.watchers[i](content);

                }

            };

            content.onChange = (callback) => {

                content.watchers.push(callback);

            };

            return content

        })();


        let getCart = () => {

            return cart;

        };


        let updateCart = (response) => {

            cart.update(response.response);

        };


        let fetch = () => {

            edge.api.get(updateCart);

            return cart.content;

        };


        let add = (itemId) => {

            edge.api.add(itemId, updateCart);

            return cart.content;

        };


        let update = (cartItem) => {

            edge.api.update(cartItem, updateCart);

            return cart.content;

        };


        let remove = (cartItem) => {

            edge.api.remove(cartItem, updateCart);

            return cart.content;

        };

        let clear = () => {

            edge.api.clear(updateCart);

            return cart.content;

        };


        let init = () => {

            fetch();

        };


        return {
            getCart,
            add,
            update,
            remove,
            clear,
            init
        }

    })()
};


document.addEventListener('DOMContentLoaded', (event) => {

    edge.cart.init();
    edge.cartDropdown.init();

});
