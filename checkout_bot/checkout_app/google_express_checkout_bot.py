# -*- coding: utf-8 -*-
import time
import logging

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from django.conf import settings

logger = logging.getLogger('google_express_logger')


class GoogleExpressCheckoutBot(object):
    accounts_url = 'https://accounts.google.com'
    email = 'chaim14251@gmail.com'
    password = 'nochum11'
    goods_url = 'https://www.google.com/express/u/0/product/' \
        '9182472493455614380_10269187404013219762_9090995?' \
        'ei=v1InWZDxHtKwigOy64PIDw&ved=0EOEqCA8'
    cart_url = 'https://www.google.com/express/u/0/cart'
    button_change_xpath = '//ul[contains(@class, "addressSelectorDropdown")]' \
        '/li/button'
    user_is_authenticated = False

    def __init__(self, *args, **kwargs):
        self.browser = webdriver.Chrome(
            executable_path=settings.DRIVER_PATH)  # PhantomJS()
        self.browser.set_window_size(1024, 768)

    def place_an_order(self):
        """Make order for specified goods
        """
        self._make_login()
        self._set_delivery_address()
        self._add_order()
        self._close_selenium_browser()

    def _make_login(self):
        """Try to authenticate with selenium browser
        """
        self.browser.get(self.accounts_url)

        self._post_email_with_selenium()
        self._post_password_with_selenium()
        self._set_if_user_authenticated()

    def _post_email_with_selenium(self):
        def wait_sign_in_page_load():
            element_exists = self._selenium_element_load_waiting(
                By.ID, 'identifierId',
                success_msg='Sign in page loaded',
                timeout_exception_msg='Timed out waiting Sign in page open')
            if element_exists:
                return True

        try:
            page_loaded = wait_sign_in_page_load()
            if not page_loaded:
                self._go_to_login_from_accounts_page()
                wait_sign_in_page_load()

            email = self.browser.find_element_by_id('identifierId')
            email.send_keys(self.email)
            button_next = self.browser.find_element_by_id('identifierNext')
            button_next.click()
        except Exception as e:
            logger.error(e)

    def _go_to_login_from_accounts_page(self):
        def wait_accounts_page_load():
            self._selenium_element_load_waiting(
                By.ID, 'identifierLink',
                success_msg='Accounts page loaded',
                timeout_exception_msg='Timed out waiting Accounts page open')

        try:
            wait_accounts_page_load()
            identifierLink = self.browser.find_element_by_id('identifierLink')
            identifierLink.click()
        except Exception as e:
            logger.error(e)

    def _post_password_with_selenium(self):
        def wait_password_page_load():
            self._selenium_element_load_waiting(
                By.NAME, 'password',
                success_msg='Password page loaded',
                timeout_exception_msg='Timed out waiting Password page open')

        try:
            wait_password_page_load()
            password = self.browser.find_element_by_name('password')
            password.send_keys(self.password)
            button_next = self.browser.find_element_by_id('passwordNext')
            button_next.click()
        except Exception as e:
            logger.error(e)

    def _set_if_user_authenticated(self):
        exception_msg = 'Timed out waiting for user authenticated page'
        elem_exists = self._selenium_element_load_waiting(
            By.CLASS_NAME, 'gbii',
            success_msg='User authenticated',
            timeout_exception_msg=exception_msg)

        if elem_exists:
            self.user_is_authenticated = True

    def _set_delivery_address(self):
        self.browser.get(self.goods_url)
        self._open_address_popup()
        address = self._choose_address_from_popup()
        if not address:
            self._add_new_address_to_list()
        #     self._choose_address_from_popup()

    def _open_address_popup(self):
        def wait_address_menu_button_load():
            excp_msg = 'Timed out waiting for Address menu button load'
            self._selenium_element_load_waiting(
                By.CLASS_NAME, 'addressDeliverToZipLabel',
                success_msg='Address menu button loaded',
                timeout_exception_msg=excp_msg)

        try:
            wait_address_menu_button_load()
            show_popup_button = self.browser.find_element_by_class_name(
                'addressDeliverToZipLabel')
            show_popup_button.click()
        except Exception as e:
            logger.error(e)

    def _choose_address_from_popup(self):
        def wait_change_address_button_load():
            excp_msg = 'Timed out waiting for change address button load'
            self._selenium_element_load_waiting(
                By.XPATH, self.button_change_xpath,
                success_msg='Change address button loaded',
                timeout_exception_msg=excp_msg)

        try:
            wait_change_address_button_load()
            text = '1061 E Hyde Park Bl'
            change_button = self.browser.find_element_by_xpath(
                '//a[contains(@class, "addressLink")]')  # contains(., "' + text + '")]')
            logger.info(change_button)
            change_button.click()
            time.sleep(10)
        except Exception as e:
            logger.error(e)

    def _add_new_address_to_list(self):
        try:
            change_address_button = self.browser.find_element_by_xpath(
                self.button_change_xpath)
            change_address_button.click()
        except Exception as e:
            logger.error(e)

    def _add_order(self):
        if self.user_is_authenticated:
            self._add_goods_to_cart()
            self._go_to_shopping_cart_and_checkout()
            self._press_on_place_order_button()

    def _add_goods_to_cart(self):
        def wait_add_to_cart_button_load():
            self._selenium_element_load_waiting(
                By.CLASS_NAME, 'addItemButton',
                success_msg='Add item button loaded',
                timeout_exception_msg='Timed out waiting for ADD BUTTON')

        try:
            wait_add_to_cart_button_load()
            add_item_button = self.browser.find_element_by_class_name(
                'addItemButton')
            add_item_button.click()
        except Exception as e:
            logger.error(e)

    def _go_to_shopping_cart_and_checkout(self):
        def wait_cart_page_load():
            self._selenium_element_load_waiting(
                By.CLASS_NAME, 'checkoutButton',
                success_msg='Cart page loaded',
                timeout_exception_msg='Timed out waiting Cart page open')

        try:
            self.browser.get(self.cart_url)
            wait_cart_page_load()
            checkout_button = self.browser.find_element_by_class_name(
                'checkoutButton')
            checkout_button.click()
        except Exception as e:
            logger.error(e)

    def _press_on_place_order_button(self):
        pass

    def _close_selenium_browser(self):
        try:
            self.browser.close()
            self.browser.quit()
            logger.info('Browser closed')
        except OSError as e:
            logger.error(e)

    def _selenium_element_load_waiting(
            self, by_selector_type, selector,
            success_msg='', timeout_exception_msg=''):
        """Wrapper around explicity waiting for
        elememt will appear in selenium browser
        """
        try:
            element_present = EC.visibility_of_element_located(
                (by_selector_type, selector))
            WebDriverWait(
                self.browser, settings.TIMEOUT_PAGE_LAODING).until(
                    element_present)
            logger.info(success_msg)
        except TimeoutException:
            logger.error(timeout_exception_msg)
            return False
        except Exception as e:
            logger.error(e)
            return False

        return True

    def save_page_to_log_if_debug(self, file_name, debug=False):
        # Write html pages to project logs dir if DEBUG setting is True
        if settings.DEBUG or debug:
            file_path = '%s/%s' % (
                settings.LOGS_DIR, file_name.replace(' ', '_'))
            logger.info('Path to employees list html file: %s' % file_path)
            try:
                page = self.browser.page_source.encode('utf-8')
            except Exception as e:
                logger.error(e)
                return None

            with open(file_path, 'w') as f:
                f.write(page)

    def save_img_to_log_if_debug(self, file_name, debug=False):
        # Save screenshot into logs dir if DEBUG setting is True
        if settings.DEBUG or debug:
            try:
                self.browser.save_screenshot(file_name)
            except Exception as e:
                logger.error(e)
