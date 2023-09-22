<?php
/*
Plugin Name: Custom Settings Plugin
Description: Этот плагин добавляет настраиваемое поле в админке WordPress.
Version: 1.0
Author: Ваше имя
*/

// Функция для добавления страницы настроек в админку
function custom_settings_page() {
    // Ваш код для создания страницы настроек здесь
    // Выводим страницу настроек в админке
    add_menu_page(
        'Custom Settings',
        'Custom Settings',
        'manage_options',
        'custom-settings',
        'display_custom_settings'
    );
}

// Функция для добавления поля настроек
function custom_settings_field() {
    // Заголовок поля настроек
    $field_title = 'Custom Field';
    
    // Получаем сохраненное значение из базы данных
    $field_value = get_option('custom_field');

    // Выводим HTML для поля
    echo '<input type="text" id="custom_field" name="custom_field" value="' . esc_attr($field_value) . '" />';
}


// Функция для сохранения значений в базе данных
function custom_settings_save() {
    // Регистрируем нашу настройку и указываем функцию для ее очистки
    register_setting('custom-settings-group', 'custom_field', 'sanitize_text_field');
}


// Функция для вывода поля настроек в админке
function display_custom_settings() {
    ?>
    <div class="wrap">
        <h2>Custom Settings</h2>
        <form method="post" action="options.php">
            <?php
            settings_fields('custom-settings-group');
            do_settings_sections('custom-settings');
            submit_button();
            ?>
        </form>
    </div>
    <?php
}

// Функция для генерации формы настроек
function custom_settings_form() {
    ?>
    <input type="text" id="custom_field" name="custom_field" value="<?php echo esc_attr(get_option('custom_field')); ?>" />
    <?php
}

// Функция для подключения стилей
function custom_settings_styles() {
    wp_enqueue_style('custom-settings-style', plugins_url('css/custom-settings.css', __FILE__));
}

// Добавляем хук для подключения стилей
add_action('admin_enqueue_scripts', 'custom_settings_styles');
// Добавляем хуки для страницы настроек и сохранения настроек
add_action('admin_menu', 'custom_settings_page');
// Добавляем хук для регистрации нашей настройки
add_action('admin_init', 'custom_settings_save');
