"""Binance Expert Application
"""
from logger import getLogger
from flask import Flask, render_template, request, flash, redirect, jsonify

app = Flask(__name__)

logger = getLogger()

if __name__ == "__main__":
    logger.info("start app")
    logger.debug("test debug")
    logger.warning("test warning")
    logger.error("test error")
    logger.critical("test critical")
    logger.info("finish app")
