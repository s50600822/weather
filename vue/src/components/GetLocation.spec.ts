import { vi } from 'vitest'
import { shallowMount } from "@vue/test-utils";
import GetLocation from "./GetLocation.vue";

describe("GetLocation", () => {
  it("should render the component without crashing", async (): Promise<void> => {
    const mockGeolocation: Geolocation = {
      getCurrentPosition: () => {}, // watever
      clearWatch: () => {},        // watever
      watchPosition: jest.fn(), // watever https://jestjs.io/docs/mock-functions
    };
    jest.spyOn(navigator, 'geolocation', 'get').mockReturnValue(mockGeolocation);
    const wrapper = await shallowMount(GetLocation);
    expect(wrapper).toBeTruthy();
  });
});
