edge = edge || {};


edge.cartDropdown = (() => {

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
                                    children: [e('span', {classes: ['fa', 'fa-trash']})]
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

        edge.cart.get().onChange((content) => {

            update(content);

        });

    };


    return {
        toggle,
        clear,
        update,
        init
    }

})();
