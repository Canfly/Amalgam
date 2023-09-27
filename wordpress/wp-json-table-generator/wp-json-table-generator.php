<?php

/**
 * The plugin bootstrap file
 *
 * This file is read by WordPress to generate the plugin information in the plugin
 * admin area. This file also includes all of the dependencies used by the plugin,
 * registers the activation and deactivation functions, and defines a function
 * that starts the plugin.
 *
 * @link              https://canfly.org/adiom
 * @since             1.0.0
 * @package           Wp_Json_Table_Generator
 *
 * @wordpress-plugin
 * Plugin Name:       wp-json-table-generator
 * Plugin URI:        https://https://github.com/Canfly/Amalgam/tree/master/wordpress/wp-json-table-generator
 * Description:       🌟 Try the JSON Table Plugin today and unlock the potential of JSON data visualization for your website! 🚀
 * Version:           1.0.0
 * Author:            Adiom Timur
 * Author URI:        https://canfly.org/adiom/
 * License:           GPL-2.0+
 * License URI:       http://www.gnu.org/licenses/gpl-2.0.txt
 * Text Domain:       wp-json-table-generator
 * Domain Path:       /languages
 */

// If this file is called directly, abort.
if ( ! defined( 'WPINC' ) ) {
	die;
}

/**
 * Currently plugin version.
 * Start at version 1.0.0 and use SemVer - https://semver.org
 * Rename this for your plugin and update it as you release new versions.
 */
define( 'WP_JSON_TABLE_GENERATOR_VERSION', '1.0.0' );

/**
 * The code that runs during plugin activation.
 * This action is documented in includes/class-wp-json-table-generator-activator.php
 */
function activate_wp_json_table_generator() {
	require_once plugin_dir_path( __FILE__ ) . 'includes/class-wp-json-table-generator-activator.php';
	Wp_Json_Table_Generator_Activator::activate();
}

/**
 * The code that runs during plugin deactivation.
 * This action is documented in includes/class-wp-json-table-generator-deactivator.php
 */
function deactivate_wp_json_table_generator() {
	require_once plugin_dir_path( __FILE__ ) . 'includes/class-wp-json-table-generator-deactivator.php';
	Wp_Json_Table_Generator_Deactivator::deactivate();
}

register_activation_hook( __FILE__, 'activate_wp_json_table_generator' );
register_deactivation_hook( __FILE__, 'deactivate_wp_json_table_generator' );

/**
 * The core plugin class that is used to define internationalization,
 * admin-specific hooks, and public-facing site hooks.
 */
require plugin_dir_path( __FILE__ ) . 'includes/class-wp-json-table-generator.php';

/**
 * Begins execution of the plugin.
 *
 * Since everything within the plugin is registered via hooks,
 * then kicking off the plugin from this point in the file does
 * not affect the page life cycle.
 *
 * @since    1.0.0
 */
function run_wp_json_table_generator() {

	$plugin = new Wp_Json_Table_Generator();
	$plugin->run();

}
run_wp_json_table_generator();
