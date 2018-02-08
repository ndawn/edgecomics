edge = edge || {};


edge.filters = {
    rub: (value) => {

        return value + 'р.';

    },

    quantity: (value) => {

        return value + 'шт.';

    }
};
