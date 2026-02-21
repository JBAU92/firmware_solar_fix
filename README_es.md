# Meshtastic nRF52 Solar Recovery Fix ☀️🔋

Este repositorio contiene versiones modificadas del firmware Meshtastic específicamente optimizadas para nodos repetidores solares basados en la arquitectura **nRF52840**. 

## 🚀 El Problema: El "Coma Profundo" Solar
Muchos usuarios de nodos RAK4631 o XIAO nRF52 sufren el mismo problema: tras varios días nublados, el nodo agota la batería y entra en un estado de sueño del que no despierta,
incluso cuando vuelve a salir el sol y la batería se recarga. Esto obliga a desplazamientos físicos para resetear el dispositivo manualmente.

## 🛠️ Solución Implementada
He auditado y modificado el flujo de gestión de energía para corregir este comportamiento:

1. **Gestión Inteligente del FSM**: Se ha redefinido el umbral de "Batería Crítica" a **3.4V**.
2. El nodo ahora entra en sueño profundo de forma controlada antes de que el voltaje caiga a niveles que provoquen inestabilidad en el regulador.
3. **Resurrección por Hardware (LPCOMP)**: Se ha activado y configurado el comparador de baja potencia del chip nRF52.
4. El hardware monitoriza el voltaje y lanza un reinicio automático (Wake-up) cuando detecta que la carga solar ha subido la batería a niveles seguros (~3.7V).

## 📂 Descargas y Hardware
Puedes encontrar los binarios `.uf2` listos para flashear en la sección de **[Releases](https://github.com/JBAU92/firmware_solar_fix/releases/tag/v1.0.0-solar-fix)**:
* **RAK4631**: Optimizado para WisBlock.
* **XIAO nRF52840**: Versión estándar y versión I2C.
* **Pro Micro DIY**: Para implementaciones personalizadas.

## ☕ Soporte
Este fix es fruto de varias horas analizando esquemáticos y el código fuente de Meshtastic para mejorar la resiliencia de nuestras redes.
Si este trabajo te ha ahorrado un viaje al tejado para resetear un nodo:

👉 **[Invítame a un café ](https://buy.stripe.com/4gM00l2Qp7V26Ye0UgbMQ00)**

Para consultorías técnicas sobre despliegue de redes Mesh profesionales o auditorías de bajo consumo, puedes contactarme por privado.
