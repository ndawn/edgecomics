edge = edge || {};


edge.cart = (() => {

    let cart = (() => {

        let content = [];

        content.watchers = [];

        content.update = (newContent) => {

            console.log(newContent);

            while (content.pop() !== undefined);

            for (let cartItem of newContent) {

                content.push(cartItem);

            }

            for (let watcher of content.watchers) {

                watcher(content);

            }

        };

        content.onChange = (callback) => {

            content.watchers.push(callback);

        };

        return content;

    })();


    let updateCart = (response) => {

        cart.update(response.response);

    };


    let get = () => {

        return cart;

    };


    let fetch = () => {

        edge.api.get(updateCart);

        return cart;

    };


    let add = (itemId) => {

        edge.api.add(itemId, updateCart);

        return cart;

    };


    let update = (cartItem) => {

        edge.api.update(cartItem, updateCart);

        return cart;

    };


    let remove = (cartItem) => {

        edge.api.remove(cartItem, updateCart);

        return cart;

    };

    let clear = () => {

        edge.api.clear(updateCart);

        return cart;

    };


    let init = () => {

        fetch();

    };


    return {
        get,
        add,
        update,
        remove,
        clear,
        init
    }

})();
