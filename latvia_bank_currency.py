# -*- coding: utf-8 -*-
# Copyright (c) 2017, Test and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document 
from datetime import date 
#from six.moves import urllib
import urllib
import xmltodict 
import shutil 

class LatviaBankCurrency(Document):
	pass 
##komentārs
@frappe.whitelist()
def download_file():
	file_name = "currencies.xml"
	try:
		url = "https://www.bank.lv/vk/ecb.xml"
		urllib.urlretrieve(url,file_name) 
	except:
		return frappe.get_traceback()

@frappe.whitelist()
def fill_doctype(fileName2): 
		download_file()
		try:
			url = "https://www.bank.lv/vk/ecb.xml"
			response = urllib.urlopen(url)
			data = response.read()
			obj = xmltodict.parse(data)
			currencies = obj["CRates"]["Currencies"] 
			for each in currencies.values():
				for each2 in each: 
					doc = frappe.get_doc({
           				'doctype':'Currency_table',
						'parent': fileName2,
           				'id': each2["ID"], 
						'currency': each2["Rate"],
           				'parenttype':'Latvia Bank Currency',
           				'parentfield':'currency_values' }) 
					doc.insert()
			doc.save()
		except:
			frappe.get_traceback()

@frappe.whitelist()
def create_new_doctype():
		try:
			new_file_name = date.today()
			doc = frappe.get_doc({
				"doctype": "Latvia Bank Currency",
					})
			doc.insert()
			try:
				fill_doctype(new_file_name)
			except: 
				frappe.get_traceback()
		except:
			frappe.get_traceback()

"""
@frappe.whitelist()
def delete_old():
		try:
			frappe.delete_doc_if_exists('Latvia Bank Currency','Currencies1')
		except:
			return frappe.get_traceback() 
"""
"""
@frappe.whitelist()
def fill_doctype2():
		path = "erpnext-bench/sites/currencies.xml"
		try:
			with open(path, "rb") as xml_file:
				try:
					content = xml_file.read()
					obj = xmltodict.parse(content)
					currencies = obj["CRates"]["Currencies"]
					for each in currencies.values():
						for each2 in each: 
							doc = frappe.get_doc({
								'doctype':'Currency_table',
								'parent': '0d753f6905',
								'id':each2["ID"], 
								'currency':each2["Rate"],
								'parenttype':'Latvia Bank Currency',
								'parentfield':'currency_values' })
							doc.insert()
					doc.save()
				except:
					return frappe.get_traceback()
		except: 
			return frappe.get_traceback()
""" 
