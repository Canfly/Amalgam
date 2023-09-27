<?php

/**
 * Define the internationalization functionality
 *
 * Loads and defines the internationalization files for this plugin
 * so that it is ready for translation.
 *
 * @link       https://canfly.org/adiom
 * @since      1.0.0
 *
 * @package    Wp_Json_Table_Generator
 * @subpackage Wp_Json_Table_Generator/includes
 */

/**
 * Define the internationalization functionality.
 *
 * Loads and defines the internationalization files for this plugin
 * so that it is ready for translation.
 *
 * @since      1.0.0
 * @package    Wp_Json_Table_Generator
 * @subpackage Wp_Json_Table_Generator/includes
 * @author     Adiom Timur <adiom@canfly.org>
 */
class Wp_Json_Table_Generator_i18n {


	/**
	 * Load the plugin text domain for translation.
	 *
	 * @since    1.0.0
	 */
	public function load_plugin_textdomain() {

		load_plugin_textdomain(
			'wp-json-table-generator',
			false,
			dirname( dirname( plugin_basename( __FILE__ ) ) ) . '/languages/'
		);

	}



}
