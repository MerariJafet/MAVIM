#!/bin/bash
# setup_mavim.sh - MAVIM Interactive Secrets Injector
# Uso: Ejecutar al inicio del proyecto para generar el archivo .env de forma segura.

echo "==============================================="
echo "  MAVIM Setup - Secure Secret Injector"
echo "==============================================="
echo "Este script configurará las variables de entorno Base."
echo "IMPORTANTE: Los agentes tienen PROHIBIDO leer el archivo .env resultante."
echo ""

ENV_FILE=".env"

# Evitar sobreescribir si ya existe
if [ -f "$ENV_FILE" ]; then
    read -p "El archivo .env ya existe. ¿Deseas sobreescribirlo? (y/n): " confirm
    if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
        echo "Operación cancelada."
        exit 0
    fi
fi

echo "Iniciando generación de secretos..."
> $ENV_FILE

# Solicitar secretos críticos
read -p "1. ¿Dominio principal de la App? (ej. api.midominio.com): " APP_DOMAIN
echo "APP_DOMAIN=$APP_DOMAIN" >> $ENV_FILE

read -s -p "2. ¿Contraseña de Base de Datos (DB_PASSWORD)?: " DB_PASSWORD
echo ""
echo "DB_PASSWORD=$DB_PASSWORD" >> $ENV_FILE

read -s -p "3. ¿Clave Secreta de Stripe (STRIPE_SECRET_KEY)?: " STRIPE_KEY
echo ""
echo "STRIPE_SECRET_KEY=$STRIPE_KEY" >> $ENV_FILE

read -s -p "4. ¿Clave de API de Inteligencia Artificial (ej. OPENAI_API_KEY)?: " AI_KEY
echo ""
echo "AI_API_KEY=$AI_KEY" >> $ENV_FILE

# Generar JWT Secret aleatorio
JWT_SECRET=$(openssl rand -hex 32 2>/dev/null || date +%s | sha256sum | base64 | head -c 32)
echo "JWT_SECRET=$JWT_SECRET" >> $ENV_FILE

echo ""
echo "==============================================="
echo "¡Archivo .env generado con éxito!"
echo "Los secretos han sido inyectados de forma segura."
echo "==============================================="
