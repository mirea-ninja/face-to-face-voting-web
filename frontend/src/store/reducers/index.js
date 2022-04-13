import * as actions from '../actions/actionsTypes'

const initialState = {
    data: null,
    isLoading: false
}

export default function userUpdate(state = initialState, { type, payload }) {
    switch (type) {
        case actions.USER_LOGGING_IN:
            return { ...initialState, isLoading: true }
        case actions.USER_LOGGED_IN:
            return { data: payload, isLoading: false }
        case actions.USER_LOGGED_OUT:
            return initialState
        default:
            return state
    }
}