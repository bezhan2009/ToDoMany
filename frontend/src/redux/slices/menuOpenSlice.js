import { createSlice } from '@reduxjs/toolkit';

const menuOpenSlice = createSlice({
  name: 'menuOpen',
  initialState: {
    isOpen: false
  },
  reducers: {
    toggleMenu: state => {
      state.isOpen = !state.isOpen;
    },
    setMenu: (state, action) => {
      state.isOpen = action.payload;
    }
  }
});

export const { toggleMenu, setMenu } = menuOpenSlice.actions;
export const selectIsMenuOpen = state => state.menuOpen.isOpen;
export default menuOpenSlice.reducer;
