<?php
/**
 * Plugin Name: My Plugin
 * Plugin URI: https://example.com/
 * Description: This is my plugin.
 * Version: 1.0
 * Author: Your Name
 * Author URI: https://example.com/
 **/

// 

function my_plugin_function() {
    echo 'Hello, World!';
}

function my_plugin_settings_page() {
?>
<div class="wrap">
    <h1><?php echo esc_html( get_admin_page_title() ); ?></h1>
    <form action="options.php" method="post">
        <?php
            settings_fields( 'my_plugin_settings_group' );
            do_settings_sections( 'my_plugin_settings_page' );
            submit_button( 'Save Settings' );
        ?>
    </form>
</div>
<?php

}

function my_plugin_add_settings() {
    add_options_page( 'My Plugin Settings', 'My Plugin', 'manage_options', 'my-plugin', 'my_plugin_settings_page' );
}

add_action( 'admin_menu', 'my_plugin_add_settings' );