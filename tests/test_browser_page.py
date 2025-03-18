import pytest
import pytest_asyncio
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch, ANY

from pydoll.browser.page import Page
from pydoll.element import WebElement
from pydoll.events import PageEvents

from pydoll.commands import (
    DomCommands,
    RuntimeCommands,
    NetworkCommands,
    StorageCommands,
    PageCommands,
    FetchCommands,
)


@pytest_asyncio.fixture
async def mock_connection_handler():
    with patch('pydoll.browser.page.ConnectionHandler', autospec=True) as mock:
        handler = mock.return_value
        handler.execute_command = AsyncMock()
        handler.register_callback = AsyncMock()
        handler.network_logs = []
        yield handler


@pytest_asyncio.fixture
async def page(mock_connection_handler):
    page = Page(connection_port=9223, page_id='test_page')
    page._connection_handler = mock_connection_handler
    return page


@pytest.mark.asyncio
async def test_page_initialization(page):
    assert page._connection_handler is not None
    assert not page.page_events_enabled
    assert not page.network_events_enabled
    assert not page.fetch_events_enabled
    assert not page.dom_events_enabled


@pytest.mark.asyncio
async def test_current_url(page):
    page._connection_handler.execute_command.return_value = {
        'result': {'result': {'value': 'https://example.com'}}
    }

    url = await page.current_url
    assert url == 'https://example.com'
    page._connection_handler.execute_command.assert_called_once_with(
        DomCommands.get_current_url(), timeout=60
    )


@pytest.mark.asyncio
async def test_page_source(page):
    page._connection_handler.execute_command.return_value = {
        'result': {'result': {'value': '<html><body>Test</body></html>'}}
    }

    source = await page.page_source
    assert source == '<html><body>Test</body></html>'
    page._connection_handler.execute_command.assert_called_once()


@pytest.mark.asyncio
async def test_get_cookies(page):
    test_cookies = [{'name': 'test', 'value': 'value'}]
    page._connection_handler.execute_command.return_value = {
        'result': {'cookies': test_cookies}
    }

    cookies = await page.get_cookies()
    assert cookies == test_cookies
    page._connection_handler.execute_command.assert_called_once_with(
        NetworkCommands.get_all_cookies(), timeout=60
    )


@pytest.mark.asyncio
async def test_set_cookies(page):
    test_cookies = [{'name': 'test', 'value': 'value'}]
    await page.set_cookies(test_cookies)
    page._connection_handler.execute_command.assert_any_call(
        NetworkCommands.set_cookies(test_cookies), timeout=60
    )
    page._connection_handler.execute_command.assert_any_call(
        StorageCommands.set_cookies(test_cookies), timeout=60
    )


@pytest.mark.asyncio
async def test_delete_all_cookies(page):
    await page.delete_all_cookies()
    assert page._connection_handler.execute_command.call_count == 2
    page._connection_handler.execute_command.assert_any_call(
        StorageCommands.clear_cookies(), timeout=60
    )
    page._connection_handler.execute_command.assert_any_call(
        NetworkCommands.clear_browser_cookies(), timeout=60
    )


@pytest.mark.asyncio
async def test_go_to_success(page):
    page._wait_page_load = AsyncMock(return_value=None)
    page._connection_handler.execute_command.return_value = {
        'result': {'result': {'value': 'https://another.com'}}
    }
    await page.go_to('https://example.com')
    page._connection_handler.execute_command.assert_called_with(
        PageCommands.go_to('https://example.com'), timeout=60
    )


@pytest.mark.asyncio
async def test_go_to_timeout(page):
    page._connection_handler.execute_command.return_value = {
        'result': {'result': {'value': 'loading'}}
    }
    page._wait_page_load = AsyncMock(
        side_effect=asyncio.TimeoutError('Timeout')
    )
    with pytest.raises(TimeoutError):
        await page.go_to('https://example.com', timeout=0)


@pytest.mark.asyncio
async def test_refresh(page):
    page._connection_handler.execute_command.side_effect = [
        {'result': {'result': {'value': 'complete'}}},
    ]
    page._wait_page_load = AsyncMock(return_value=None)
    await page.refresh()
    page._connection_handler.execute_command.assert_called_with(
        PageCommands.refresh(), timeout=60
    )


@pytest.mark.asyncio
async def test_get_screenshot(page, tmp_path):
    test_image = b'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/wcAAgAB/edzE+oAAAAASUVORK5CYII='
    page._connection_handler.execute_command.return_value = {
        'result': {'data': test_image.decode()}
    }

    screenshot_path = tmp_path / 'screenshot.png'
    with patch('aiofiles.open') as mock_open:
        mock_open.return_value.__aenter__.return_value.write = AsyncMock()
        await page.get_screenshot(str(screenshot_path))

    page._connection_handler.execute_command.assert_called_once_with(
        PageCommands.screenshot(), timeout=60
    )


@pytest.mark.asyncio
async def test_enable_events(page):
    await page.enable_page_events()
    assert page.page_events_enabled
    page._connection_handler.execute_command.assert_called_once_with(
        PageCommands.enable_page(), timeout=60
    )

    await page.enable_network_events()
    assert page.network_events_enabled
    page._connection_handler.execute_command.assert_any_call(
        NetworkCommands.enable_network_events(), timeout=60
    )

    await page.enable_fetch_events()
    assert page.fetch_events_enabled
    page._connection_handler.execute_command.assert_any_call(
        FetchCommands.enable_fetch_events(False, 'Document'), timeout=60
    )

    await page.enable_dom_events()
    assert page.dom_events_enabled
    page._connection_handler.execute_command.assert_any_call(
        DomCommands.enable_dom_events(), timeout=60
    )


@pytest.mark.asyncio
async def test_disable_events(page):
    await page.disable_fetch_events()
    assert not page.fetch_events_enabled
    page._connection_handler.execute_command.assert_called_once_with(
        FetchCommands.disable_fetch_events(), timeout=60
    )

    await page.disable_page_events()
    assert not page.page_events_enabled
    page._connection_handler.execute_command.assert_any_call(
        PageCommands.disable_page(), timeout=60
    )


@pytest.mark.asyncio
async def test_execute_script(page):
    test_script = 'return document.title'
    page._connection_handler.execute_command.return_value = {
        'result': {'result': {'value': 'Test Page'}}
    }

    result = await page.execute_script(test_script)
    page._connection_handler.execute_command.assert_called_once_with(
        RuntimeCommands.evaluate_script(test_script), timeout=60
    )

    # Test with element context
    element = WebElement(
        object_id='test_id', connection_handler=page._connection_handler
    )
    await page.execute_script('argument.click()', element)
    page._connection_handler.execute_command.assert_called_with(
        RuntimeCommands.call_function_on(
            'test_id', 'function(){ this.click() }', return_by_value=True
        ),
        timeout=60,
    )


@pytest.mark.asyncio
async def test_get_network_logs(page):
    page._connection_handler.network_logs = [
        {'params': {'request': {'url': 'https://example.com/api'}}},
        {'params': {'request': {'url': 'https://example.com/other'}}},
    ]

    logs = await page.get_network_logs(['api'])
    assert len(logs) == 1
    assert logs[0]['params']['request']['url'] == 'https://example.com/api'

    with pytest.raises(LookupError):
        await page.get_network_logs(['nonexistent'])


@pytest.mark.asyncio
async def test_get_network_response_body(page):
    page._connection_handler.execute_command.return_value = {
        'result': {'body': '{"key": "value"}', 'base64Encoded': False}
    }

    body, encoded = await page.get_network_response_body('request_id')
    assert body == '{"key": "value"}'
    assert not encoded
    page._connection_handler.execute_command.assert_called_once_with(
        NetworkCommands.get_response_body('request_id'), timeout=60
    )


@pytest.mark.asyncio
async def test_has_dialog(page):
    page._connection_handler.dialog = {'params': {'type': 'alert'}}

    result = await page.has_dialog()
    assert result is True

    page._connection_handler.dialog = None
    result = await page.has_dialog()
    assert result is False


@pytest.mark.asyncio
async def test_get_dialog_message(page):
    page._connection_handler.dialog = {'params': {'message': 'Test message'}}

    message = await page.get_dialog_message()
    assert message == 'Test message'

    page._connection_handler.dialog = None
    with pytest.raises(LookupError):
        await page.get_dialog_message()


@pytest.mark.asyncio
async def test_accept_dialog(page):
    page._connection_handler.dialog = {'params': {'type': 'alert'}}
    await page.accept_dialog()
    page._connection_handler.execute_command.assert_called_once_with(
        PageCommands.handle_dialog(True), timeout=60
    )


@pytest.mark.asyncio
async def test_accept_dialog_no_dialog(page):
    page._connection_handler.dialog = None
    with pytest.raises(LookupError):
        await page.accept_dialog()


@pytest.mark.asyncio
async def test_go_to_same_url(page):
    page._connection_handler.execute_command.return_value = {
        'result': {'result': {'value': 'https://example.com'}}
    }
    page._wait_page_load = AsyncMock(return_value=None)
    await page.go_to('https://example.com')
    page._connection_handler.execute_command.assert_called_with(
        PageCommands.refresh(), timeout=60
    )


@pytest.mark.asyncio
async def test_refresh_timeout(page):
    page._wait_page_load = AsyncMock(
        side_effect=asyncio.TimeoutError('Timeout')
    )
    with pytest.raises(TimeoutError):
        await page.refresh()


@pytest.mark.asyncio
async def test_set_download_path(page):
    await page.set_download_path('/tmp')
    page._connection_handler.execute_command.assert_called_once_with(
        PageCommands.set_download_path('/tmp'), timeout=60
    )


@pytest.mark.asyncio
async def test_get_pdf_base64(page):
    response = {'result': {'data': 'test_pdf'}}
    page._connection_handler.execute_command.return_value = response
    pdf = await page.get_pdf_base64()
    assert pdf == 'test_pdf'
    page._connection_handler.execute_command.assert_called_once_with(
        PageCommands.print_to_pdf(), timeout=60
    )


@pytest.mark.asyncio
async def test_print_to_pdf(page):
    response = {
        'result': {
            'data': 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/wcAAgAB/edzE+oAAAAASUVORK5CYII='
        }
    }
    page._connection_handler.execute_command.return_value = response
    with patch('aiofiles.open') as mock_open:
        mock_open.return_value.__aenter__.return_value.write = AsyncMock()
        await page.print_to_pdf('/tmp/test.pdf')
        page._connection_handler.execute_command.assert_called_once_with(
            PageCommands.print_to_pdf('/tmp/test.pdf'), timeout=60
        )


@pytest.mark.asyncio
async def test_get_network_logs(page):
    page._connection_handler.network_logs = [
        {'params': {'request': {'url': 'https://example.com/request'}}},
        {'params': {'otherkey': {}}},
    ]

    logs = await page.get_network_logs(['request'])
    assert logs[0]['params']['request']['url'] == 'https://example.com/request'

    with pytest.raises(LookupError):
        await page.get_network_logs(['nonexistent'])


@pytest.mark.asyncio
async def test_get_network_response_bodies(page):
    page._connection_handler.network_logs = [
        {
            'params': {
                'request': {'url': 'https://example.com/api'},
                'requestId': 'request_id',
            }
        },
        {
            'params': {
                'request': {'url': 'https://example.com/other'},
                'requestId': 'other_id',
            }
        },
    ]
    page.get_network_response_body = AsyncMock(
        return_value=('{"key": "value"}', False)
    )
    matches = ['api']

    responses = await page.get_network_response_bodies(matches)
    assert responses[0] == {'key': 'value'}

    with pytest.raises(LookupError):
        await page.get_network_response_bodies(['nonexistent'])


@pytest.mark.asyncio
async def test_get_network_response_bodies_keyerror(page):
    page._connection_handler.network_logs = [
        {'params': {'request': {'url': 'https://example.com/api'}}},
        {'params': {'request': {'url': 'https://example.com/other'}}},
    ]

    matches = ['api']

    assert await page.get_network_response_bodies(matches) == []


@pytest.mark.asyncio
async def test__wait_page_load(page):
    page._connection_handler.execute_command.return_value = {
        'result': {'result': {'value': 'complete'}}
    }
    await page._wait_page_load()
    page._connection_handler.execute_command.assert_called_once_with(
        RuntimeCommands.evaluate_script('document.readyState'), timeout=60
    )


@pytest.mark.asyncio
async def test__wait_page_load_timeout(page):
    page._connection_handler.execute_command.return_value = {
        'result': {'result': {'value': 'loading'}}
    }

    with patch('pydoll.browser.page.asyncio.sleep', AsyncMock()):
        with pytest.raises(asyncio.TimeoutError):
            await page._wait_page_load(timeout=0.1)


@pytest.mark.asyncio
async def test_enable_intercept_file_chooser_dialog(page):
    await page.enable_intercept_file_chooser_dialog()
    assert page.intercept_file_chooser_dialog_enabled
    page._connection_handler.execute_command.assert_called_once_with(
        PageCommands.set_intercept_file_chooser_dialog(True), timeout=60
    )


@pytest.mark.asyncio
async def test_disable_intercept_file_chooser_dialog(page):
    await page.disable_intercept_file_chooser_dialog()
    assert not page.intercept_file_chooser_dialog_enabled
    page._connection_handler.execute_command.assert_called_once_with(
        PageCommands.set_intercept_file_chooser_dialog(False), timeout=60
    )


@pytest.mark.asyncio
async def test_expect_file_chooser(page):
    files = ['file1.txt', 'file2.txt']
    async with page.expect_file_chooser(files=files):
        assert page.page_events_enabled
        assert page.intercept_file_chooser_dialog_enabled
        page._connection_handler.register_callback.assert_called_with(
            PageEvents.FILE_CHOOSER_OPENED, ANY, True
        )
    assert not page.intercept_file_chooser_dialog_enabled
    await page.disable_intercept_file_chooser_dialog()
    assert not page.intercept_file_chooser_dialog_enabled

