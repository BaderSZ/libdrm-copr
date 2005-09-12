# Makefile for source rpm: libdrm
# $Id$
NAME := libdrm
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
