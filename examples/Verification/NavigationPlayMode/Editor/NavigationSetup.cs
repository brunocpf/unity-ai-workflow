#nullable enable
using UnityEditor;
using UnityEngine;
using UnityEngine.UIElements;

public static class NavigationSetup
{
    public static void Configure()
    {
        var settings = new SerializedObject(
            AssetDatabase.LoadAllAssetsAtPath("ProjectSettings/ProjectSettings.asset")[0]);
        settings.FindProperty("activeInputHandler").intValue = 1;
        settings.ApplyModifiedPropertiesWithoutUndo();
        var panel = ScriptableObject.CreateInstance<PanelSettings>();
        panel.themeStyleSheet = AssetDatabase.LoadAssetAtPath<ThemeStyleSheet>(
            "Assets/NavigationTests/Resources/Navigation.tss");
        AssetDatabase.CreateAsset(panel, "Assets/NavigationTests/Resources/NavigationPanel.asset");
        AssetDatabase.SaveAssets();
    }
}
