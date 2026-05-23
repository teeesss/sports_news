import pytest
from engine.stealth_navigator import StealthNavigator

@pytest.mark.asyncio
async def test_stealth_navigator_user_agent_version_alignment():
    """Verify that userAgentData brands version matches the user agent version."""
    # Test with custom user agent to check dynamic version extraction
    custom_ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
    nav = StealthNavigator(headless=True)
    nav.current_ua = custom_ua
    await nav.initialize()
    
    try:
        page = await nav.context.new_page()
        # Evaluate navigator.userAgentData on the page
        brands = await page.evaluate("() => navigator.userAgentData.brands")
        
        # Extract version from current UA
        import re
        match = re.search(r'Chrome/(\d+)\.', custom_ua)
        assert match is not None, f"Could not find Chrome version in User-Agent: {custom_ua}"
        expected_version = match.group(1)
        
        # Assert that the version in brands matches the expected version
        for brand in brands:
            if brand['brand'] in ['Google Chrome', 'Chromium']:
                assert brand['version'] == expected_version, f"Expected brand version to be '{expected_version}' for {brand['brand']}, but got '{brand['version']}'"
    finally:
        await nav.close()
