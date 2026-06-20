document.addEventListener("DOMContentLoaded", () => {
    const tabs = document.querySelectorAll(".tab");
    const contents = document.querySelectorAll(".tab-content");
    const form = document.querySelector("#form-simulador");
    const messageBox = document.querySelector("#mensaje-formulario");

    const modeloSelect = document.querySelector("#modelo");
    const planSelect = document.querySelector("#plan");

    const resumenModelo = document.querySelector("#resumen-modelo");
    const resumenPrecio = document.querySelector("#resumen-precio");
    const resumenImagen = document.querySelector("#resumen-imagen");
    const resumenPlan = document.querySelector("#resumen-plan");
    const resumenCuotas = document.querySelector("#resumen-cuotas");
    const resumenAdjudicacion = document.querySelector("#resumen-adjudicacion");
    const resumenRetiro = document.querySelector("#resumen-retiro");
    const resumenTasa = document.querySelector("#resumen-tasa");
    const resumenCuota = document.querySelector("#resumen-cuota");

    const retiro = 500000;
    const cuotas = 84;
    const tasa = 14.5;

    let dolarOficial = null;

    function obtenerCardPorModelo(modelo) {
        return [...document.querySelectorAll(".model-card")]
            .find(card => card.dataset.modelo === modelo);
    }

    function actualizarCardSeleccionada(modelo) {
        document.querySelectorAll(".model-card").forEach(card => {
            card.classList.remove("selected");

            const boton = card.querySelector("button");
            if (boton) {
                boton.textContent = "Seleccionar";
            }
        });

        const cardSeleccionada = obtenerCardPorModelo(modelo);

        if (cardSeleccionada) {
            cardSeleccionada.classList.add("selected");

            const boton = cardSeleccionada.querySelector("button");
            if (boton) {
                boton.textContent = "Seleccionado";
            }
        }
    }

    function obtenerPrecioVehiculo() {
        const cardDelModelo = obtenerCardPorModelo(modeloSelect.value);
        return cardDelModelo ? Number(cardDelModelo.dataset.precio) : 0;
    }

    tabs.forEach((tab, index) => {
        tab.addEventListener("click", () => {
            tabs.forEach(t => t.classList.remove("active"));
            tab.classList.add("active");

            contents.forEach(c => c.classList.remove("active"));
            contents[index].classList.add("active");
        });
    });

    document.querySelectorAll(".model-card").forEach(card => {
        card.addEventListener("click", () => {
            modeloSelect.value = card.dataset.modelo;
            actualizarCardSeleccionada(card.dataset.modelo);
            actualizarResumen();
        });
    });

    modeloSelect.addEventListener("change", () => {
        actualizarCardSeleccionada(modeloSelect.value);
        actualizarResumen();
    });

    planSelect.addEventListener("change", () => {
        actualizarResumen();
    });

    function formatearPesos(valor) {
        return new Intl.NumberFormat("es-AR", {
            style: "currency",
            currency: "ARS",
            maximumFractionDigits: 0,
        }).format(valor);
    }

    function formatearDolares(valor) {
        return new Intl.NumberFormat("es-AR", {
            style: "currency",
            currency: "USD",
            maximumFractionDigits: 2,
        }).format(valor);
    }

    function calcularPlan() {
        const porcentajeAdjudicacion = planSelect.value === "Plan 70/30" ? 0.30 : 0.40;
        const precioVehiculo = obtenerPrecioVehiculo();
        const adjudicacion = precioVehiculo * porcentajeAdjudicacion;
        const montoFinanciado = precioVehiculo - adjudicacion;
        const montoTotal = (montoFinanciado + retiro) * (1 + tasa / 100);
        const cuotaMensual = montoTotal / cuotas;

        return {
            adjudicacion,
            cuotaMensual,
        };
    }

    function actualizarResumen() {
        const calculo = calcularPlan();
        const cardDelModelo = obtenerCardPorModelo(modeloSelect.value);

        resumenModelo.textContent = modeloSelect.value;
        resumenPrecio.textContent = formatearPesos(obtenerPrecioVehiculo());
        resumenPlan.textContent = planSelect.value;
        resumenCuotas.textContent = cuotas;
        resumenAdjudicacion.textContent = formatearPesos(calculo.adjudicacion);
        resumenRetiro.textContent = formatearPesos(retiro);
        resumenTasa.textContent = `${tasa.toFixed(2).replace(".", ",")}%`;
        resumenCuota.textContent = formatearPesos(calculo.cuotaMensual);

        if (cardDelModelo) {
            resumenImagen.src = cardDelModelo.dataset.imagen;
            resumenImagen.alt = modeloSelect.value;
        }
    }

    async function cargarDolarOficial() {
        try {
            const response = await fetch("/cotizacion-dolar/");
            const data = await response.json();

            if (data.ok) {
                dolarOficial = data.dolar_oficial;
            }
        } catch (error) {
            dolarOficial = null;
        }
    }

    function mostrarEquivalenciaDolar(input) {
        const valor = Number(input.value);
        const info = document.querySelector(`[data-dolar-for="${input.id}"]`);

        if (!info || !valor || !dolarOficial) {
            if (info) {
                info.textContent = "";
            }
            return;
        }

        const equivalente = valor / dolarOficial;

        info.textContent = `Este importe equivale a ${formatearDolares(equivalente)} bajo la cotización del dólar oficial del día ($${dolarOficial}).`;
    }

    ["ingreso_neto", "garante_ingreso_neto"].forEach(id => {
        const input = document.querySelector(`#${id}`);

        if (input) {
            input.addEventListener("input", () => {
                mostrarEquivalenciaDolar(input);
            });
        }
    });

    function mostrarMensaje(texto, tipo) {
        messageBox.textContent = texto;
        messageBox.className = `message-box ${tipo}`;
    }

    function mostrarTabDelCampo(campo) {
        const contenido = campo.closest(".tab-content");

        if (!contenido) {
            return;
        }

        const index = [...contents].indexOf(contenido);

        if (index === -1) {
            return;
        }

        tabs.forEach(t => t.classList.remove("active"));
        contents.forEach(c => c.classList.remove("active"));

        tabs[index].classList.add("active");
        contents[index].classList.add("active");
    }

    function enfocarCampoConError(campo) {
        mostrarTabDelCampo(campo);

        setTimeout(() => {
            campo.focus();
        }, 100);
    }

    function validarFormularioCliente() {
        const obligatorios = form.querySelectorAll("[required]");

        for (const campo of obligatorios) {
            if (!campo.value.trim()) {
                mostrarMensaje("Completá todos los campos obligatorios antes de simular.", "error");
                enfocarCampoConError(campo);
                return false;
            }
        }

        const nombreInput = document.querySelector("#nombre");
        const garanteNombreInput = document.querySelector("#garante_nombre");
        const dniInput = document.querySelector("#dni");
        const emailInput = document.querySelector("#email");
        const telefonoInput = document.querySelector("#telefono");
        const ingresoNetoInput = document.querySelector("#ingreso_neto");
        const garanteIngresoNetoInput = document.querySelector("#garante_ingreso_neto");
        const fechaNacimientoInput = document.querySelector("#fecha_nacimiento");
        const garanteFechaNacimientoInput = document.querySelector("#garante_fecha_nacimiento");
        const garanteAntiguedadInput = document.querySelector("#garante_antiguedad");

        const nombre = nombreInput.value.trim();
        const garanteNombre = garanteNombreInput.value.trim();
        const dni = dniInput.value.trim();
        const email = emailInput.value.trim();
        const telefono = telefonoInput.value.trim();
        const ingresoNeto = Number(ingresoNetoInput.value);
        const garanteIngresoNeto = Number(garanteIngresoNetoInput.value);
        const garanteAntiguedad = Number(garanteAntiguedadInput.value);

        const regexNombre = /^[A-Za-zÁÉÍÓÚáéíóúÑñÜü\s]+$/;
        const regexDni = /^\d{7,8}$/;
        const regexTelefono = /^[\d\s()+-]{8,20}$/;
        const regexEmail = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

        if (!regexNombre.test(nombre)) {
            mostrarMensaje("El nombre solo puede contener letras y espacios.", "error");
            enfocarCampoConError(nombreInput);
            return false;
        }

        if (!regexDni.test(dni)) {
            mostrarMensaje("El DNI debe tener 7 u 8 números.", "error");
            enfocarCampoConError(dniInput);
            return false;
        }

        if (!fechaNacimientoInput.value) {
            mostrarMensaje("Ingresá la fecha de nacimiento del titular.", "error");
            enfocarCampoConError(fechaNacimientoInput);
            return false;
        }

        if (!regexEmail.test(email)) {
            mostrarMensaje("Ingresá un correo electrónico válido.", "error");
            enfocarCampoConError(emailInput);
            return false;
        }

        if (!regexTelefono.test(telefono)) {
            mostrarMensaje("El teléfono solo puede contener números, espacios, paréntesis, + o -.", "error");
            enfocarCampoConError(telefonoInput);
            return false;
        }

        if (ingresoNeto <= 0) {
            mostrarMensaje("El ingreso neto debe ser mayor a 0.", "error");
            enfocarCampoConError(ingresoNetoInput);
            return false;
        }

        if (!regexNombre.test(garanteNombre)) {
            mostrarMensaje("El nombre del garante solo puede contener letras y espacios.", "error");
            enfocarCampoConError(garanteNombreInput);
            return false;
        }

        if (!garanteFechaNacimientoInput.value) {
            mostrarMensaje("Ingresá la fecha de nacimiento del garante.", "error");
            enfocarCampoConError(garanteFechaNacimientoInput);
            return false;
        }

        if (garanteIngresoNeto <= 0) {
            mostrarMensaje("El ingreso neto del garante debe ser mayor a 0.", "error");
            enfocarCampoConError(garanteIngresoNetoInput);
            return false;
        }

        if (garanteAntiguedad < 0) {
            mostrarMensaje("La antigüedad laboral del garante no puede ser negativa.", "error");
            enfocarCampoConError(garanteAntiguedadInput);
            return false;
        }

        return true;
    }

    form.addEventListener("submit", async event => {
        event.preventDefault();

        if (!validarFormularioCliente()) {
            return;
        }

        const botonSubmit = form.querySelector('button[type="submit"]');
        botonSubmit.disabled = true;
        botonSubmit.textContent = "Procesando...";

        mostrarMensaje("Procesando la solicitud, por favor esperá unos segundos.", "info");

        const formData = new FormData(form);

        try {
            const response = await fetch(form.action, {
                method: "POST",
                body: formData,
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                },
            });

            let data;

            try {
                data = await response.json();
            } catch (error) {
                mostrarMensaje("El servidor devolvió una respuesta inválida. Revisá la consola de Django.", "error");
                return;
            }

            if (!data.ok) {
                mostrarMensaje(data.mensaje || "Hubo un error al procesar la solicitud.", "error");
                return;
            }

            const informe = data.informe;

            resumenModelo.textContent = informe.modelo;
            resumenPrecio.textContent = formatearPesos(informe.precio_vehiculo);
            resumenPlan.textContent = informe.plan;
            resumenCuotas.textContent = informe.cantidad_cuotas;
            resumenAdjudicacion.textContent = formatearPesos(informe.importe_adjudicacion);
            resumenRetiro.textContent = formatearPesos(informe.importe_retiro);
            resumenTasa.textContent = `${informe.tasa_interes.toFixed(2).replace(".", ",")}%`;
            resumenCuota.textContent = formatearPesos(informe.cuota_mensual);

            mostrarMensaje(data.mensaje, "success");

            form.reset();
            actualizarCardSeleccionada(modeloSelect.value);
            actualizarResumen();
        } catch (error) {
            mostrarMensaje("No se pudo conectar con el servidor.", "error");
        } finally {
            botonSubmit.disabled = false;
            botonSubmit.textContent = "Simular plan";
        }
    });

    cargarDolarOficial();
    actualizarCardSeleccionada(modeloSelect.value);
    actualizarResumen();
});